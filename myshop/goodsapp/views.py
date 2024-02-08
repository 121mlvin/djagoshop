from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Item, Purchase, Refund
from .forms import NewItemForm, EditProductForm

class ProductListView(ListView):
    model = Item
    template_name = 'product_list.html'
    context_object_name = 'items'
@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Item
    template_name = 'product_detail.html'
    context_object_name = 'item'

@login_required
def purchase_product_success(request, product_id):
    print("Reached the purchase_product_success view")
    item = get_object_or_404(Item, pk=product_id)
    purchases = Purchase.objects.filter(product=item)

    if request.method == 'POST':
        print("Received a POST request")
        quantity = int(request.POST.get('quantity', 0))
        print(f"Quantity: {quantity}")

        try:
            user = request.user
            if quantity > item.quantity_available:
                messages.error(request, 'Insufficient quantity available.')
            elif user.wallet < quantity * item.price:
                messages.error(request, 'Insufficient funds in your wallet.')
            else:
                purchase = Purchase.objects.create(user=user, product=item, quantity=quantity)
                item.quantity_available -= quantity
                item.save()
                user.wallet -= quantity * item.price
                user.save()
                messages.success(request, f'Successfully purchased {quantity} {item.name}(s).')
        except AttributeError:
            messages.error(request, 'User not found.')

    total_amount = 0
    if purchases:
        total_amount = purchases[0].quantity * purchases[0].product.price

    return render(request, 'purchase_product_success.html', {'purchases': purchases, 'total_amount': total_amount})

@method_decorator(login_required, name='dispatch')
class PurchasedItemsView(View):
    def get(self, request, *args, **kwargs):
        user_purchases = Purchase.objects.filter(user=request.user)
        for purchase in user_purchases:
            purchase.total_amount = purchase.quantity * purchase.product.price

        return render(request, 'purchased_items.html', {'purchases': user_purchases})


@method_decorator(login_required, name='dispatch')
class RefundProductView(View):
    def post(self, request, purchase_id):
        purchase = get_object_or_404(Purchase, pk=purchase_id)

        if timezone.now() > purchase.purchase_time + timezone.timedelta(minutes=3):
            messages.error(request, 'Refund period has expired.')
        else:
            Refund.objects.create(purchase=purchase, request_time=timezone.now, approved=False)
            messages.success(request, 'Refund requested successfully.')

        return redirect('purchased_items')

@method_decorator(staff_member_required, name='dispatch')
class AddProductView(View):
    template_name = 'add_product.html'

    def get(self, request):
        form = NewItemForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, self.template_name, {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class EditProductView(View):
    template_name = 'edit_product.html'

    def get(self, request, product_id):
        product = get_object_or_404(Item, pk=product_id)
        form = EditProductForm(instance=product)
        return render(request, self.template_name, {'form': form, 'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Item, pk=product_id)
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, self.template_name, {'form': form, 'product': product})


@method_decorator(staff_member_required, name='dispatch')
class ViewReturnsView(ListView):
    model = Refund
    template_name = 'view_returns.html'
    context_object_name = 'return_requests'

@method_decorator(staff_member_required, name='dispatch')
class ApproveReturnView(View):
    template_name = 'refund_approval.html'

    def get(self, request, refund_id):
        refund = get_object_or_404(Refund, pk=refund_id)
        return render(request, self.template_name, {'refund': refund})

    def post(self, request, refund_id):
        refund = get_object_or_404(Refund, pk=refund_id)
        action = request.POST.get('action')

        if action == 'accept':
            refund.approved = True
            refund.save()

            user = refund.purchase.user
            user.wallet += refund.purchase.quantity * refund.purchase.product.price
            user.save()

            refund.purchase.product.quantity_available += refund.purchase.quantity
            refund.purchase.product.save()

        elif action == 'deny':
            refund.approved = False
            refund.save()

        return render(request, self.template_name, {'refund': refund})

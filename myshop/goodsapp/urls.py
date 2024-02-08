from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/purchase/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/purchase/<int:product_id>/success/', purchase_product_success, name='purchase_product_success'),
    path('purchased/', PurchasedItemsView.as_view(), name='purchased_items'),
    path('product/return/<int:purchase_id>/', RefundProductView.as_view(), name='return_product'),
    path('admin/products/add/', AddProductView.as_view(), name='add_product'),
    path('admin/products/edit/<int:product_id>/', EditProductView.as_view(), name='edit_product'),
    path('admin/returns/', ViewReturnsView.as_view(), name='view_returns'),
    path('admin/returns/approve/<int:refund_id>/', ApproveReturnView.as_view(), name='approve_return'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

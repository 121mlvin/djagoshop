from django.http import HttpResponse
from django.shortcuts import render
from goodsapp.models import Item


def main(request):
    items = Item.objects.all().order_by('-id')[:3]
    return render(request, 'main_page.html', {'items': items})

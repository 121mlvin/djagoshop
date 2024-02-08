from django.contrib import admin
from .models import Item, Purchase, Refund

admin.site.register(Item)
admin.site.register(Purchase)
admin.site.register(Refund)


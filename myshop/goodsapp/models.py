from django.db import models
from userapp.models import CustomUser


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='item_images/', null=True, blank=True)
    quantity_available = models.PositiveIntegerField()

    def __str__(self):
        return f"Product: {self.name}, price: {self.price}"


class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} bought {self.product}, amount:{self.quantity}"


class Refund(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Refund #{self.id} - {self.approved}"

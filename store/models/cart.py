from django.db import models
from .product import Product

class Cart(models.Model):
    phone = models.CharField(max_length=15)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='upload/cart/', null=True, blank=True)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)

    class Meta:
        unique_together = ('phone', 'product')   # prevents duplicates

    def __str__(self):
        return f"{self.product.name} ({self.phone})"

    
from django.db import models
from .product import Product

STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On the way", "On the way"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
)

class OrderDetails(models.Model):
    phone = models.CharField(max_length=15)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    ordered_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    def __str__(self):
        return f"{self.product.name} - {self.phone}"



from django.db import models
from .category import Category


class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category , on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='upload/products/')
    @classmethod
    def get_all_product(cls):
        return cls.objects.all()
    @staticmethod
    def get_all_product_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_product()
        
    def __str__(self):
        return self.name

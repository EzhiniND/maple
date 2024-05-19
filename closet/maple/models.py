from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
class Category(models.Model):
    product_name = models.CharField(max_length=250, primary_key=True)
    category = models.CharField(max_length=50, default="", null=True)  # Corrected to lowercase
    subcategory = models.CharField(max_length=50, default="", null=True)
    description = models.CharField(max_length=800, null=True)
    price = models.IntegerField(default=0, null=True)
    image = models.ImageField(upload_to='static/img', default="", null=True)

    def __str__(self):
       if self.product_name:
          return self.product_name
       else:
          return "Unnamed Category"  

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.ManyToManyField(CartItem)
    created_at = models.DateTimeField(auto_now_add=True)
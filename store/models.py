from doctest import FAIL_FAST
from hashlib import blake2b
from math import fabs
from django.db import models
from django.contrib.auth.models import User
class ProductCategory(models.Model):
    category = models.CharField(max_length=50)  
    image = models.ImageField(blank=False)

    def __str__(self) -> str:
        return self.category 

class Products(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,null=True,blank=False)
    name = models.CharField(max_length=50,blank=False,null=False)
    price = models.PositiveIntegerField(blank=False,null=False)
    details = models.TextField(blank=True)
    image_01 = models.ImageField()
    image_02 = models.ImageField()
    image_03 = models.ImageField()

    def __str__(self) -> str:
        return self.name


class WishList(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE,null=False,blank=False)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def sub_total(self):
        sub_total=self.quantity * self.product_id.price
        return sub_total

    @property
    def grand_total(self):
            pass


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=False)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50,default='Pending')
    payment_mode = models.CharField(max_length=50) 
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE,null=True,blank=False)
    quantity = models.PositiveIntegerField(default=0,null=False,blank=False)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    name = models.CharField(max_length=150,null=False,blank=False)       
    mobile_no = models.PositiveIntegerField(null=False,blank=False)
    email = models.EmailField(max_length=254,null=True,blank=False)
    address_line1 = models.CharField(max_length=150,null=False,blank=False)
    address_line2 = models.CharField(max_length=150,null=False,blank=False)
    city = models.CharField(max_length=50,null=False,blank=False)
    state = models.CharField(max_length=50,null=False,blank=False)
    pincode = models.PositiveIntegerField(null=False,blank=False)
    country = models.CharField(max_length=50,null=False,blank=False)

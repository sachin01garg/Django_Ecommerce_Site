from django.contrib import admin
from .models import Products,ProductCategory,WishList,Cart,Order,ShippingAddress

admin.site.register(Products)
admin.site.register(ProductCategory)
admin.site.register(WishList)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(ShippingAddress)
from django.contrib import admin
from .models import User_data, Catagories,Sub_Catagory,Products, Add_to_Cart, Order, Orders_items

# Register your models here.
admin.site.register(User_data)
admin.site.register(Catagories)
admin.site.register(Sub_Catagory)
admin.site.register(Products)
admin.site.register(Add_to_Cart)
admin.site.register(Order)
admin.site.register(Orders_items)

from django.contrib import admin
from .models import Catogery, Food, Cart, CartItem, Order ,Username

admin.site.register(Catogery)
admin.site.register(Food)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Username)

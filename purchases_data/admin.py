from django.contrib import admin
from .models import User, Category, Product, Purchase, PurchaseUnit

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(PurchaseUnit)

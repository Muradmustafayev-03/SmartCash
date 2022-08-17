from django.contrib import admin
from .models import User, Category, Product, Purchase, PurchaseUnit, Store

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(PurchaseUnit)
admin.site.register(Store)

from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import User, Category, Store, Product, Purchase, PurchaseUnit


@admin.register(User)
class SortableUserAdmin(SortableAdminMixin, admin.ModelAdmin):
    ordering = []
    list_display = ['FIN']


@admin.register(Category)
class SortableCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    ordering = []
    list_display = ['title', 'description']


@admin.register(Store)
class SortableStoreAdmin(SortableAdminMixin, admin.ModelAdmin):
    ordering = []
    list_display = ['name', 'type']


@admin.register(Product)
class SortableProductAdmin(SortableAdminMixin, admin.ModelAdmin):
    ordering = []
    list_display = ['title', 'manufacturer']


@admin.register(Purchase)
class SortablePurchaseAdmin(SortableAdminMixin, admin.ModelAdmin):
    ordering = []
    list_display = ['user', 'store', 'date', 'time', 'total_payed']


@admin.register(PurchaseUnit)
class SortablePurchaseUnitAdmin(SortableAdminMixin, admin.ModelAdmin):
    ordering = []
    list_display = ['purchase', 'product', 'amount']

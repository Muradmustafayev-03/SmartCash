from django.db import models


class User(models.Model):
    FIN = models.CharField(verbose_name='Fərdi İdentifikasiya Nömrəsi (FİN)', max_length=7, default='FIN_UNKNOWN',
                           unique=True)

    def __str__(self):
        return self.FIN


class Category(models.Model):
    title = models.CharField(verbose_name='Category Title', max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Store(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    taxpayer_name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, default=None, null=True)
    is_manufacturer = models.BooleanField(null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.DecimalField(max_digits=17, decimal_places=3, blank=True, null=True)
    quantity_marker = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=17, decimal_places=2, blank=True, null=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    store = models.ForeignKey(Store, default=None, on_delete=models.DO_NOTHING)
    date = models.DateField()
    time = models.TimeField()
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    discount = models.DecimalField(max_digits=15, decimal_places=2)
    total_payed = models.DecimalField(max_digits=15, decimal_places=2)
    cashless = models.BooleanField()

    def __str__(self):
        return str(self.user) + '-' + self.store.name + '-' + str(self.date) + '-' + str(self.time)


class PurchaseUnit(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    amount = models.FloatField()

    def __str__(self):
        return str(self.purchase) + '-' + str(self.product)

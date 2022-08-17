# Generated by Django 4.1 on 2022-08-17 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PurchasesData', '0004_alter_store_is_manufacturer_alter_store_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='categories',
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity_marker',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=17),
        ),
    ]

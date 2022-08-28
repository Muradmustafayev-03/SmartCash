# Generated by Django 4.1 on 2022-08-28 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PurchasesData', '0009_alter_product_options_alter_purchase_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchaseunit',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='purchaseunit',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
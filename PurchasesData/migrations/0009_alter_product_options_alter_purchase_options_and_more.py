# Generated by Django 4.1 on 2022-08-28 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PurchasesData', '0008_alter_store_options_store_my_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='purchase',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='store',
            options={'ordering': ['order']},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='my_order',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='purchase',
            old_name='my_order',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='store',
            old_name='my_order',
            new_name='order',
        ),
    ]

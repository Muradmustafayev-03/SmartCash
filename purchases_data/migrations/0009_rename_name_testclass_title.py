# Generated by Django 3.2.9 on 2022-07-30 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchases_data', '0008_auto_20220731_0033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testclass',
            old_name='name',
            new_name='title',
        ),
    ]

# Generated by Django 3.2.9 on 2022-07-30 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases_data', '0007_testclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='testclass',
            name='name',
            field=models.CharField(default='name', max_length=50),
        ),
        migrations.AlterField(
            model_name='testclass',
            name='size',
            field=models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], max_length=323, verbose_name='weeed'),
        ),
    ]
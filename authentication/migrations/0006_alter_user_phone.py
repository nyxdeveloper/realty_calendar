# Generated by Django 3.2.4 on 2021-06-04 17:12

import authentication.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20210604_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=15, unique=True, validators=[authentication.validators.validate_phone], verbose_name='Номер телефона'),
        ),
    ]

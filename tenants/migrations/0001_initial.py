# Generated by Django 3.2.4 on 2021-06-04 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=15, verbose_name='Номер телефона')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('email', models.CharField(max_length=100, verbose_name='Email')),
                ('comment', models.TextField(verbose_name='Примечание')),
            ],
            options={
                'verbose_name': 'Съемщик',
                'verbose_name_plural': 'Съемщики',
            },
        ),
    ]

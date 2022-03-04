# Generated by Django 3.2.4 on 2021-06-11 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tenant',
            options={'ordering': ['-id'], 'verbose_name': 'Съемщик', 'verbose_name_plural': 'Съемщики'},
        ),
        migrations.AddField(
            model_name='tenant',
            name='blacklist',
            field=models.BooleanField(blank=True, default=False, verbose_name='Черный список'),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Номер телефона'),
        ),
    ]

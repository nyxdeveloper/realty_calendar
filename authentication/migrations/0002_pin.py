# Generated by Django 3.2 on 2021-05-18 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('phone', models.CharField(max_length=13, primary_key=True, serialize=False, unique=True)),
                ('code', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Пин',
                'verbose_name_plural': 'Пинкоды',
            },
        ),
    ]

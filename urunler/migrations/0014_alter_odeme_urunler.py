# Generated by Django 4.1.7 on 2023-07-19 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urunler', '0013_odeme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='odeme',
            name='urunler',
            field=models.ManyToManyField(to='urunler.sepet'),
        ),
    ]

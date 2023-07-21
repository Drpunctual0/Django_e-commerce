# Generated by Django 4.1.7 on 2023-07-20 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('urunler', '0022_remove_urun_resim_delete_resim_urun_resim'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ekleyen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('urun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urunler.urun')),
            ],
        ),
    ]

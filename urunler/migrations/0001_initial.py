# Generated by Django 4.1.7 on 2023-07-17 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AltAltKategori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AltKategori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Urun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=100)),
                ('aciklama', models.TextField(max_length=500)),
                ('fiyat', models.IntegerField()),
                ('resim', models.FileField(null=True, upload_to='urunler/')),
                ('alt_alt_kategori', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='urunler.altaltkategori')),
                ('alt_kategori', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='urunler.altkategori')),
                ('kategori', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='urunler.kategori')),
            ],
        ),
        migrations.AddField(
            model_name='altkategori',
            name='altkategori',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urunler.kategori'),
        ),
        migrations.AddField(
            model_name='altaltkategori',
            name='altkategori',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urunler.altkategori'),
        ),
        migrations.AddField(
            model_name='altaltkategori',
            name='kategori',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urunler.kategori'),
        ),
    ]
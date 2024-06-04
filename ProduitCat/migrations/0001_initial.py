# Generated by Django 4.1.13 on 2024-06-03 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('CatId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('ProdId', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('imageProd', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProduitCat.category')),
            ],
        ),
    ]

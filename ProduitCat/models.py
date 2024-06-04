from django.db import models

# Create your models here.

class Category(models.Model):
    CatId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    ProdId = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    description = models.TextField(null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE)
    imageProd = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.nom
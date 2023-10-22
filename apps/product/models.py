from django.db import models

from apps.base.models import BaseModel

# Create your models here.


class Category(BaseModel):
    category = models.CharField(
        max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.category


class Product(BaseModel):
    product = models.CharField(
        max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, name=False)
    image = models.ImageField(upload_to='product/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.product

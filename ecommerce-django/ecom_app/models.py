from itertools import product

from django.db import models

# Create your models here.
class  Categories(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Customers(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "Customers"

class Products(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=244, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    #sale stuff
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}-{self.price}$"

    class Meta:
        verbose_name_plural = "Products"

class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=14, default='', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{product}-{self.quantity}-->{self.address}"

    class Meta:
        verbose_name_plural = "Orders"
from django.db import models
from django.contrib.auth.models import User
from app_goods.models import Product


class Order(models.Model):
    createdAt = models.DateField(auto_now=True)
    fullName = models.CharField("Full name", max_length=200, null=True)
    email = models.EmailField(default="anonim@mail.ru")
    phone = models.CharField("Phone", max_length=12, null=True)
    deliveryType = models.CharField("Способ доставки", max_length=100, null=True)
    paymentType = models.CharField("Способ оплаты", max_length=100, null=True)
    totalCost = models.FloatField(default=1, blank=True)
    status = models.CharField("Статус заказа", max_length=100, null=True)
    city = models.CharField("Город", max_length=200, null=True)
    address = models.CharField("Адрес", max_length=200, null=True)
    products = models.ManyToManyField(Product, related_name="products")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Payment(models.Model):
    number = models.CharField("Number", max_length=100, null=True)
    name = models.CharField("Name", max_length=100, null=True)
    month = models.CharField("Month", max_length=20, null=True)
    year = models.CharField("Year", max_length=20, null=True)
    code = models.CharField("Code", max_length=100, null=True)

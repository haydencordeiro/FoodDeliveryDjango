
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    aadharNo = models.IntegerField(default=0)

    def __str__(self):
        return "%s's profile" % self.user


class ShopLocality(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=500)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    currentOffer = models.IntegerField()

    def __str__(self):
        return self.name


class CustomerOrder(models.Model):
    orderFor = models.OneToOneField(
        CustomerProfile, on_delete=models.CASCADE, blank=True)
    orderFrom = models.OneToOneField(
        Shop, on_delete=models.CASCADE, blank=True)
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, blank=True)

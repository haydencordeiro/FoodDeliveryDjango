
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


class Shop(models.Model):
    name = models.CharField(max_length=500)
    currentOffer = models.IntegerField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500)
    price = models.IntegerField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class CustomerOrder(models.Model):
    orderFor = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True)
    onTheWay = models.BooleanField(default=False, blank=True)
    delivered = models.BooleanField(default=False, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)

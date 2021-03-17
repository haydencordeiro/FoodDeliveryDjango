
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    # aadharNo = models.IntegerField(default=0)
    phoneNo = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return "%s's profile" % self.user


class DeliveryProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    # aadharNo = models.IntegerField(default=0)
    phoneNo = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return "%s's profile" % self.user


class ShopLocality(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=500)
    currentOffer = models.IntegerField()
    ShopImg = models.CharField(max_length=1000, blank=True)
    locality = models.ForeignKey(
        ShopLocality, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500)
    price = models.FloatField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, null=True)
    productImage = models.CharField(
        max_length=1000, default="https://i.imgur.com/K1zmsYt.jpg")

    def __str__(self):
        return self.name


class PaymentCategory(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class CustomerOrder(models.Model):
    orderFor = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True)
    product = models.ManyToManyField(
        Product, blank=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=1000, null=True)
    orderPrice = models.FloatField(default=100)
    deliveryboy = models.ForeignKey(
        DeliveryProfile, on_delete=models.CASCADE, null=True, blank=True)
    locality = models.ForeignKey(
        ShopLocality, on_delete=models.CASCADE, null=True, blank=True)
    addressinwords = models.CharField(
        max_length=1000, default="")
    typeOfPayment = models.ForeignKey(
        PaymentCategory, on_delete=models.CASCADE, null=True)

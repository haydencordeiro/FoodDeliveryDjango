
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_init
import requests


def sendNotification(usertoken, title, body):
    userdata = {
        "to": str(usertoken),
        "notification": {
            "body": str(title),
            "title": str(body),
            "content_available": True,
            "priority": "high"
        }

    }
    headers = {
        "Authorization": "key=AAAAwVFO9Fw:APA91bHymQMWRKlGHZOVMxp4_-0HA5vOlybPEpCU7NHOs1v9lkkd5JrtYzsU_3UYH5-nxcSZYA9xUOVYfpyKPE_YFdL2BgCKUvbIBBNuqfvIAOcbjLZ6eQ7o4SCAFG1UGBp8X7JnB2HI",
        "Content-Type": "application/json"

    }
    r = requests.post(
        'https://fcm.googleapis.com/fcm/send',  json=userdata, headers=headers)


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
    vendor = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=500)
    currentOffer = models.FloatField()
    ShopImg = models.CharField(max_length=1000, blank=True)
    locality = models.ForeignKey(
        ShopLocality, on_delete=models.CASCADE, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    addressinwords = models.CharField(
        max_length=1000, default="")
    phoneNo = models.CharField(max_length=10, blank=True)
    email = models.CharField(max_length=10, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)

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
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)
    orderImg = models.CharField(max_length=1000, null=True)
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

    @staticmethod
    def post_save(sender, **kwargs):
        instance = kwargs.get('instance')
        created = kwargs.get('date')
        if instance.previous_status != instance.status or created:
            print("status changed")

            user = FireabaseToken.objects.filter(
                user=instance.orderFor).first()
            usertoken = user.token
            vendor = FireabaseToken.objects.filter(
                user=instance.shop.vendor).first()
            vendortoken = vendor.token
            status = instance.status
            if status == "shoppending":
                sendNotification(vendortoken, 'New Order',
                                 "A new order has been placed")
            elif status == "shopreject":
                sendNotification(
                    usertoken, 'Order Staus', "Your order has been denied")
            elif status == "pending":
                sendNotification(usertoken, 'Order Status',
                                 "Your order is beign prepared")
            elif status == "inorder":
                sendNotification(usertoken, 'Order Staus',
                                 "Your order is on the way")
            elif status == "delivered":
                sendNotification(usertoken, 'Order Status',
                                 "You have recived your order")

    @staticmethod
    def remember_status(sender, **kwargs):
        instance = kwargs.get('instance')
        instance.previous_status = instance.status


post_save.connect(CustomerOrder.post_save, sender=CustomerOrder)
post_init.connect(CustomerOrder.remember_status, sender=CustomerOrder)


class FireabaseToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.token

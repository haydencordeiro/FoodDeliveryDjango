from rest_framework import serializers
from .models import *
from datetime import datetime
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        models = User
        fields = '__all__'


class CustomerProfileSerializer(serializers.ModelSerializer):
    # userR = UserSerializer(source='user_set', many=True)

    class Meta:
        model = CustomerProfile
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(CustomerProfileSerializer,
                    self).to_representation(instance)
        for i in instance.user._meta.fields:
            if i.name != "password":
                rep[str(i.name)] = getattr(instance.user, str(i.name))

        try:
            rep["last_login"] = instance.user.last_login.strftime(
                '%y-%m-%d %a %I:%M:%S')
        except:
            pass
        return rep


class DeliveryProfileSerializer(serializers.ModelSerializer):
    # userR = UserSerializer(source='user_set', many=True)

    class Meta:
        model = DeliveryProfile
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(DeliveryProfileSerializer,
                    self).to_representation(instance)
        for i in instance.user._meta.fields:
            if i.name != "password":
                rep[str(i.name)] = getattr(instance.user, str(i.name))

        try:
            rep["last_login"] = instance.user.last_login.strftime(
                '%y-%m-%d %a %I:%M:%S')
        except:
            pass
        return rep


class ShopLocalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopLocality
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    locality = ShopLocalitySerializer()

    class Meta:
        model = Shop
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(ProductSerializer,
                    self).to_representation(instance)
        for i in instance.shop._meta.fields:
            if i.name != "locality":
                rep["shop"+str(i.name)] = getattr(instance.shop, str(i.name))
            rep["shoplocality"] = instance.shop.locality.name
        return rep


class CustomerOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    # locality = ShopLocalitySerializer()

    class Meta:
        model = CustomerOrder
        fields = '__all__'
        # depth = 1

    def to_representation(self, instance):
        rep = super(CustomerOrderSerializer,
                    self).to_representation(instance)
        rep['customersName'] = instance.orderFor.first_name
        rep['customerPhoneNo'] = CustomerProfile.objects.get(
            user=instance.orderFor).phoneNo
        rep['locality'] = instance.locality.name
        t = str(instance.time).split(':')

        d = datetime.strptime(t[0]+":"+t[1], "%H:%M")
        rep['time'] = d.strftime("%I:%M %p")

        return rep

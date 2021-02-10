from rest_framework import serializers
from .models import *

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

    class Meta:
        model = CustomerOrder
        fields = '__all__'
        # depth = 1

    def to_representation(self, instance):
        rep = super(CustomerOrderSerializer,
                    self).to_representation(instance)

        # for i in instance.orderFrom._meta.fields:
        #     rep["orderFrom"+str(i.name)] = getattr(instance.user, str(i.name))
        # for i in instance.product._meta.fields:
        #     rep["product"+str(i.name)] = getattr(instance.product, str(i.name))

        return rep

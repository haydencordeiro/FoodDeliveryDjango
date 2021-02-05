from rest_framework import serializers
from .models import *

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        models = User
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    # userR = UserSerializer(source='user_set', many=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(UserProfileSerializer, self).to_representation(instance)
        for i in instance.user._meta.fields:
            if i.name != "password":
                rep[str(i.name)] = getattr(instance.user, str(i.name))
        return rep

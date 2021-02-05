from django.shortcuts import render
from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
import time
from rest_framework.parsers import JSONParser
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse
from django.http import (HttpResponse, HttpResponseNotFound, Http404,
                         HttpResponseRedirect, HttpResponsePermanentRedirect)
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import auth
import requests
from django.core.mail import send_mail
from rest_framework import status
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, date
from django.core.mail import send_mail
import json
from django.core.serializers.json import DjangoJSONEncoder
import os
from django.views.decorators.cache import cache_control
from django.db.models import Sum
import collections
import json
from datetime import date
from django.contrib.auth.models import User


class CustomerProfileView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        user = CustomerProfile.objects.first()
        serializer = CustomerProfileSerializer(user)
        return Response(serializer.data)


@ api_view(('GET', 'POST'))
def RegisterNewUserCustomer(request):
    temp = request.data.copy()
    if len(User.objects.filter(email=temp['email'])) > 0:
        return Response({'Error': 'Already Registered with this email'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    if len(User.objects.filter(username=temp['username'])) > 0:
        return Response({'Error': 'This username already exist'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    if len(CustomerProfile.objects.filter(aadharNo=temp['aadharNo'])) > 0:
        return Response({'Error': 'Already Registered with this aadhar'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    try:
        tempUser = User(
            username=temp['username'],
            first_name=temp['first_name'],
            last_name=temp['last_name'],
            email=temp['email'],
        )
        tempUser.set_password(temp['password'])
        tempUser.save()
        tempCustomerProfile = CustomerProfile(user=tempUser,
                                              aadharNo=temp['aadharNo'], )
        tempCustomerProfile.save()
    except:
        return Response(temp, status=status.HTTP_400_BAD_REQUEST)
    return Response(CustomerProfileSerializer(tempCustomerProfile).data, status=status.HTTP_201_CREATED)

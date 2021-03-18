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
from django.db.models import Count, Sum


class CustomerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        try:
            user = CustomerProfile.objects.get(user=request.user)
        except:
            pass
        serializer = CustomerProfileSerializer(user)
        return Response(serializer.data)


class DeliveryProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        try:
            user = DeliveryProfile.objects.get(user=request.user)
        except:
            pass
        serializer = DeliveryProfileSerializer(user)
        return Response(serializer.data)


@api_view(('GET',))
@ permission_classes([IsAuthenticated])
def WhoAmI(request):
    data = {

    }
    temp = CustomerProfile.objects.filter(user=request.user)
    if len(temp) > 0:
        data['iam'] = "customer"
        return HttpResponse(json.dumps(data), status=status.HTTP_200_OK)
    else:
        data['iam'] = "deliveryboy"
        return HttpResponse(json.dumps(data), status=status.HTTP_200_OK)


@ api_view(('POST',))
def RegisterNewUserCustomer(request):
    temp = request.data.copy()
    if len(User.objects.filter(email=temp['email'])) > 0:
        return Response({'Error': 'Already Registered with this email'}, status=status.HTTP_400_BAD_REQUEST)
    if len(User.objects.filter(username=temp['username'])) > 0:
        return Response({'Error': 'This username already exist'}, status=status.HTTP_400_BAD_REQUEST)
    # if len(CustomerProfile.objects.filter(aadharNo=temp['aadharNo'])) > 0:
    #     return Response({'Error': 'Already Registered with this aadhar'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    try:
        tempUser = User(
            username=temp['username'],
            first_name=temp['full_name'],
            email=temp['email'],
        )
        tempUser.set_password(temp['password'])
        tempUser.save()
        tempCustomerProfile = CustomerProfile(
            user=tempUser,
            phoneNo=temp['phoneNo']
        )
        tempCustomerProfile.save()
    except:
        return Response(temp, status=status.HTTP_400_BAD_REQUEST)
    return Response(CustomerProfileSerializer(tempCustomerProfile).data, status=status.HTTP_201_CREATED)


@ api_view(('POST',))
def RegisterNewUserDeliveryBoy(request):
    temp = request.data.copy()
    if len(User.objects.filter(email=temp['email'])) > 0:
        return Response({'Error': 'Already Registered with this email'}, status=status.HTTP_400_BAD_REQUEST)
    if len(User.objects.filter(username=temp['username'])) > 0:
        return Response({'Error': 'This username already exist'}, status=status.HTTP_400_BAD_REQUEST)
    # if len(CustomerProfile.objects.filter(aadharNo=temp['aadharNo'])) > 0:
    #     return Response({'Error': 'Already Registered with this aadhar'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    try:
        tempUser = User(
            username=temp['username'],
            first_name=temp['full_name'],
            email=temp['email'],
        )
        tempUser.set_password(temp['password'])
        tempUser.save()
        tempDeliveryProfile = DeliveryProfile(
            user=tempUser,
            phoneNo=temp['phoneNo']
        )
        tempDeliveryProfile.save()
    except:
        return Response(temp, status=status.HTTP_400_BAD_REQUEST)
    return Response(DeliveryProfileSerializer(tempDeliveryProfile).data, status=status.HTTP_201_CREATED)


@ api_view(('GET',))
@ permission_classes([IsAuthenticated])
def LoggedInCustomerOrders(request):
    temp = CustomerOrder.objects.filter(
        orderFor=request.user).order_by('-date').order_by('-time')
    return Response(CustomerOrderSerializer(temp, many=True).data, status=status.HTTP_200_OK)


@ api_view(('GET',))
@ permission_classes([IsAuthenticated])
def CustomerPendingOrders(request):
    temp = CustomerOrder.objects.filter(
        orderFor=request.user).filter(status="pending")
    return Response(CustomerOrderSerializer(temp, many=True).data, status=status.HTTP_200_OK)


@ api_view(('GET',))
@ permission_classes([IsAuthenticated])
def ListAllShops(request):
    temp = Shop.objects.all()
    return Response(ShopSerializer(temp, many=True).data, status=status.HTTP_200_OK)


@ api_view(('GET',))
@ permission_classes([IsAuthenticated])
def ListAllProducts(request):
    temp = Product.objects.all()
    return Response(ProductSerializer(temp, many=True).data, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def CustomerBuyProduct(request):
    data = request.data.copy()
    tempProductList = []
    temp = CustomerOrder(
        orderFor=request.user,
        orderImg=data['orderImg'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        status=data['status'],
        addressinwords=data["addressinwords"],
        typeOfPayment=PaymentCategory.objects.filter(
            name=data["typeOfPayment"]).first(),
        shop=Shop.object.filter(id=int(data["shopID"])).first()

    )
    temp.save()

    for i in list(data['productId']):
        if i != '[' or i != ']':
            try:
                temp.product.add(Product.objects.get(id=i))
            except:
                pass
    temp.save()

    return Response(CustomerOrderSerializer(temp).data, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def CustomerCancelProduct(request):
    data = request.data.copy()
    temp = CustomerOrder.objects.filter(id=data['productId'])
    temp.delete()
    return Response(CustomerOrderSerializer(temp).data, status=status.HTTP_200_OK)


@ api_view(('GET', 'POST'))
@ permission_classes([IsAuthenticated])
def DeliveryPendingOrders(request):
    if request.method == "GET":
        temp = CustomerOrder.objects.filter(status="pending")
        return Response(CustomerOrderSerializer(temp, many=True).data, status=status.HTTP_200_OK)
    else:
        data = request.data.copy()
        temp = CustomerOrder.objects.get(id=data['orderID'])
        temp.deliveryboy = DeliveryProfile.objects.get(user=request.user)
        temp.status = data['status']
        temp.save()
        return Response(CustomerOrderSerializer(temp).data, status=status.HTTP_200_OK)


@ api_view(('GET', 'POST'))
@ permission_classes([IsAuthenticated])
def DeliveryinorderOrders(request):
    if request.method == "GET":
        temp = CustomerOrder.objects.filter(deliveryboy=DeliveryProfile.objects.get(
            user=request.user)).filter(status="inorder")
        return Response(CustomerOrderSerializer(temp, many=True).data, status=status.HTTP_200_OK)
    # else:
        # data = request.data.copy()
        # temp = CustomerOrder.objects.get(id=data['orderID'])
        # temp.deliveryboy = DeliveryProfile.objects.get(user=request.user)
        # temp.status = data['status']
        # return Response(CustomerOrderSerializer(temp).data, status=status.HTTP_200_OK)


# Vendor


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def AddProduct(request):
    data = request.data.copy()

    temp = Product(

        name=data['name'],
        price=float(data['price']),
        shop=Shop.objects.get(id=int(data["shop"])),
        category=ProductCategory.objects.get(id=int(data["category"])),
        productImage=data['productImage'],


    )
    temp.save()

    return Response(ProductSerializer(temp).data, status=status.HTTP_200_OK)


@ api_view(('GET',))
@ permission_classes([IsAuthenticated])
def ListAllProductCategories(request):
    temp = ProductCategory.objects.all()
    return Response(ProductCategorySerializer(temp, many=True).data, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def UpdateOrderStatus(request):
    temp = CustomerOrder.objects.filter(
        id=int(request.data["orderID"])).first()
    temp.status = request.data["status"]
    temp.save()
    return Response(CustomerOrderSerializer(temp).data, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def AddShop(request):
    data = request.data
    temp = Shop(
        name=data["name"],
        currentOffer=float(data["currentOffer"]),
        ShopImg=data["ShopImg"],
        locality=ShopLocality.objects.filter(id=int(data["locality"])).first(),
        latitude=float(data["latitude"]),
        longitude=float(data["longitude"]),
        addressinwords=data["addressinwords"],
        phoneNo=data["phoneNo"],
        email=data["email"],

    )

    temp.save()
    return Response(ShopSerializer(temp).data, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def AllProductsOfShop(request):
    data = request.data
    temp = Product.objects.filter(
        shop=Shop.objects.filter(id=data["shopID"]).first())
    return Response(ProductSerializer(temp, many=True).data, status=status.HTTP_200_OK)


@ api_view(('POST', 'GET'))
@ permission_classes([IsAuthenticated])
def FirebaseTokenView(request):
    if request.method == "GET":
        return Response(FireabaseTokenSerializer(FireabaseToken.objects.all(), many=True).data, status=status.HTTP_200_OK)
    else:
        data = request.data
        temp = FireabaseToken(
            token=request.data["token"]
        )
        temp.save()
        return Response(FireabaseTokenSerializer(temp).data, status=status.HTTP_200_OK)


@ api_view(('POST',))
# @ permission_classes([IsAuthenticated])
def ShopAnalysis(request):
    shopID = int(request.data['shopID'])
    temp = CustomerOrder.objects.filter(shop=Shop.objects.filter(
        id=shopID).first()).values('date').annotate(price=Sum('orderPrice'))
    dates = [i['date'] for i in temp]
    price = [i['price'] for i in temp]

    return Response({"dates": dates, "prices": price}, status=status.HTTP_200_OK)

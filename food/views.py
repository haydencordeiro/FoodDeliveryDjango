from re import S
import re
from django.db.models.signals import pre_init
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
import datetime
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth, TruncYear
import requests
import json
import random
from django.db.models import Q


def getFoodImageURL(foodName):
    headers = {
        "Authorization": "563492ad6f917000010000013784e527f0764d279ff0e8157222e0d2",
        "Content-Type": "application/json"

    }
    r = requests.get(
        'https://api.pexels.com/v1/search?query={}&per_page=1'.format(foodName), headers=headers)
    data = r.json()
    try:
        return (random.choice(data["photos"])['src']['original']+"?auto=compress")
    except:
        return "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress"


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
    vendor = Shop.objects.filter(vendor=request.user)
    temp = CustomerProfile.objects.filter(user=request.user)
    delb = DeliveryProfile.objects.filter(user=request.user)
    if len(vendor) > 0:
        data['iam'] = "vendor"
        return HttpResponse(json.dumps(data), status=status.HTTP_200_OK)

    elif len(temp) > 0:
        data['iam'] = "customer"
        return HttpResponse(json.dumps(data), status=status.HTTP_200_OK)

    elif len(delb) > 0:
        data['iam'] = "deliveryboy"
        return HttpResponse(json.dumps(data), status=status.HTTP_200_OK)
    elif request.user.is_staff:
        data['iam'] = "admin"
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
        orderFor=request.user).filter(Q(status="pending") | Q(status="shoppending") | Q(status="delivered")).order_by(*['-date', '-time'])

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
        orderImg=getFoodImageURL("food"),
        latitude=data['latitude'],
        longitude=data['longitude'],
        status=data['status'],
        addressinwords=data["addressinwords"],
        typeOfPayment=PaymentCategory.objects.filter(
            name=data["typeOfPayment"]).first(),
        shop=Shop.objects.filter(id=int(data["shopID"])).first(),
        locality=Shop.objects.filter(id=int(data["shopID"])).first().locality,
        orderPrice=float(data["orderPrice"])

    )
    temp.save()
    productIDS = data['productId'].split(',')
    try:
        quan = data['productQuan'].split(',')
    except:
        quan = []
    for idx, i in enumerate(productIDS):

        try:
            pro = Product.objects.get(id=int(i))
            temp.product.add(pro)
            new = ProductQuanities(
                product=pro,
                quantity=int(quan[idx]),
                orderID=temp

            )
            new.save()

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
        shop=Shop.objects.get(id=int(data["shopID"])),
        category=ProductCategory.objects.get(id=int(data["category"])),
        productImage=getFoodImageURL(data['name']),


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
        vendor=request.user,
        name=data["name"],
        currentOffer=float(data["currentOffer"]),
        ShopImg=getFoodImageURL('restaurent'),
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
        temp = FireabaseToken.objects.filter(user=request.user).first()
        if temp is None:

            temp = FireabaseToken(
                user=request.user,
                token=request.data["token"]
            )
        else:
            temp.token = request.data["token"]
        temp.save()

        return Response(FireabaseTokenSerializer(temp).data, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def ShopAnalysis(request):
    shopID = int(request.data['shopID'])
    # weekly
    today = datetime.today().weekday()
    sunday = datetime.today() - timedelta(days=today+1)
    last_week = [["Sun", 0, 0], ["Mon", 0, 0], ["Tue", 0, 0], [
        "Wed", 0, 0], ["Thu", 0, 0], ["Fri", 0, 0], ["Sat", 0, 0]]
    for i in range(today+2):
        temp = CustomerOrder.objects.filter(shop=Shop.objects.filter(
            id=shopID).first()).filter(date=sunday).values("date").annotate(price=Sum('orderPrice')).annotate(c=Count('id'))

        try:
            last_week[i] = [last_week[i][0], temp[0]["c"], temp[0]["price"]]
        except:
            pass

        sunday += timedelta(days=1)

    # monthly
    name_months = [("Jan", 0, 0), ("Feb", 0, 0), ("March", 0, 0), ("April", 0, 0), ("May", 0, 0), ("June", 0, 0),
                   ("July", 0, 0), ("August", 0, 0), ("Sept", 0, 0), ("Oct", 0, 0), ("Nov", 0, 0), ("Dec", 0, 0)]
    month = CustomerOrder.objects.filter(shop=Shop.objects.filter(id=shopID).first()).annotate(
        month=TruncMonth('date')).values('month').annotate(price=Sum('orderPrice')).annotate(c=Count('id'))

    for i in month:
        if(date.today().year == i['month'].year):
            name_months[i['month'].month] = (
                name_months[i['month'].month][0], i["c"], i["price"])
    # print(name_months)
    # yearly
    name_year = [[i, 0, 0]
                 for i in range(date.today().year, date.today().year-3, -1)]

    years = CustomerOrder.objects.filter(shop=Shop.objects.filter(id=shopID).first()).annotate(
        year=TruncYear('date')).values('year').annotate(price=Sum('orderPrice')).annotate(c=Count('id'))[:3]
    for j, i in enumerate(years):
        name_year[j] = [name_year[j][0], i["c"], i["price"]]
    # print(name_year)
    return Response({"last_week": last_week, "months": name_months, "year": name_year}, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def UpdateShopDetails(request):
    data = request.data
    shop = Shop.objects.filter(id=int(data["shopID"])).first()
    shop.currentOffer = float(data["currentOffer"])
    shop.save()

    return Response(ShopSerializer(shop).data, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def DeleteProduct(request):
    data = request.data
    product = Product.objects.filter(id=int(data["prodID"])).first()
    product.delete()

    return Response({}, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def UpdateProduct(request):
    data = request.data
    product = Product.objects.filter(id=int(data["prodID"])).first()
    product.name = data["name"]
    product.price = data["price"]

    product.save()

    return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)


@ api_view(('GET',))
@ permission_classes([IsAuthenticated])
def LoggedInVendorShop(request):
    data = request.data
    shop = Shop.objects.filter(vendor=request.user).first()
    return Response(ShopSerializer(shop).data, status=status.HTTP_200_OK)


@ api_view(('GET',))
@ permission_classes([IsAuthenticated])
def VendorsShopOrders(request):
    data = request.data
    shop = Shop.objects.filter(vendor=request.user).first()
    orders = CustomerOrder.objects.filter(shop=shop)
    return Response(CustomerOrderSerializer(orders, many=True).data, status=status.HTTP_200_OK)


@ api_view(('GET',))
@ permission_classes([IsAuthenticated])
def SingleShopDetails(request):
    shop = Shop.objects.filter(vendor=request.user).first()
    return Response(ShopSerializer(shop).data, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def SingleShopAllProducts(request):
    shop = Shop.objects.filter(id=int(request.data["shopID"])).first()
    products = Product.objects.filter(shop=shop)
    return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def UpdateUserDetails(request):
    data = request.data
    customer = CustomerProfile.objects.filter(user=request.user).first()
    customer.phoneNo = data["phoneNo"]
    customer.user.first_name = data["first_name"]
    return Response(CustomerProfileSerializer(customer).data, status=status.HTTP_200_OK)

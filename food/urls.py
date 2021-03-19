
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from food import views
from rest_framework import routers
from .views import *
from rest_framework import routers


urlpatterns = [


    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('api/whoami/', WhoAmI,
         name='WhoAmI'),
    path('api/userinfo/', CustomerProfileView.as_view(),
         name='CustomerProfileView'),
    path('api/deliveryboyinfo/', DeliveryProfileView.as_view(),
         name='DeliveryProfileView'),
    path('api/createcustomer/', RegisterNewUserCustomer,
         name='RegisterNewUserCustomer'),
    path('api/createdeliveryboy/', RegisterNewUserDeliveryBoy,
         name='RegisterNewUserDeliveryBoy'),

    path('api/loggedincustomerorders/', LoggedInCustomerOrders,
         name='LoggedInCustomerOrders'),

    path('api/customerpendingorders/', CustomerPendingOrders,
         name='CustomerPendingOrders'),

    path('api/listallshops/', ListAllShops,
         name='ListAllShops'),

    path('api/listallproducts/', ListAllProducts,
         name='ListAllProducts'),

    path('api/customerbuyproduct/', CustomerBuyProduct,
         name='CustomerBuyProduct'),
    path('api/customercancelproduct/', CustomerCancelProduct,
         name='CustomerCancelProduct'),


    path('api/deliveryboypendingorders/', DeliveryPendingOrders,
         name='DeliveryPendingOrders'),
    path('api/deliveryboyinorderorders/', DeliveryinorderOrders,
         name='DeliveryinorderOrders'),


    # vendor
    path('api/addproduct/', AddProduct,
         name='AddProduct'),
    path('api/allproductcategories/', ListAllProductCategories,
         name='ListAllProductCategories'),


    path('api/updateorderstatus/', UpdateOrderStatus,
         name='UpdateOrderStatus'),

    path('api/addshop/', AddShop,
         name='AddShop'),
    path('api/allproductsshop/', AllProductsOfShop,
         name='AllProductsOfShop'),

    path('api/firebasetoken/', FirebaseTokenView,
         name='FirebaseTokenView'),


    path('api/shopanalysis/', ShopAnalysis,
         name='ShopAnalysis'),



    path('api/updateshopdetails/', UpdateShopDetails,
         name='UpdateShopDetails'),


    path('api/deleteproduct/', DeleteProduct,
         name='DeleteProduct'),
    path('api/updateproduct/', UpdateProduct,
         name='UpdateProduct'),

    path('api/loggedinvendorshop/', LoggedInVendorShop,
         name='LoggedInVendorShop'),



    path('api/vendorshoporder/', VendorsShopOrders,
         name='VendorsShopOrders'),




]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

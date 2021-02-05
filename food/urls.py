
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
    path('api/userinfo/', UserProfileView.as_view(), name='UserProfileView'),
    path('api/createcustomer/', RegisterNewUserCustomer,
         name='RegisterNewUserCustomer'),
    # path('api/', include(router.urls)),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

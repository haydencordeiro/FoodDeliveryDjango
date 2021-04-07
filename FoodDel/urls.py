from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url


urlpatterns = [
    path('userdetails/admin/', admin.site.urls),
    path('', include('food.urls')),
    path('api/password_reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),

]

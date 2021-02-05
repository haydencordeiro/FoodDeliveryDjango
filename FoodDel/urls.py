from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url


urlpatterns = [
    path('', include('food.urls')),
    path('admin/', admin.site.urls),
    path('api/password_reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),

]

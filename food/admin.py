from django.contrib import admin
from .models import *

from django.apps import apps


# models = apps.get_models()

# for model in models:
#     try:
#         admin.site.register(model)
#     except:
#         pass

admin.site.index_title = "Food Delviery"
admin.site.site_header = "Food Delviery"
admin.site.site_title = "Food Delviery"


class StoreImageListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in StoreImage._meta.fields if True]


admin.site.register(StoreImage, StoreImageListAdmin)


class ProductQuanitiesListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in ProductQuanities._meta.fields if True]


admin.site.register(ProductQuanities, ProductQuanitiesListAdmin)


class FireabaseTokenListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in FireabaseToken._meta.fields if True]


admin.site.register(FireabaseToken, FireabaseTokenListAdmin)


class CustomerProfileListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in CustomerProfile._meta.fields if True]


admin.site.register(CustomerProfile, CustomerProfileListAdmin)


class PaymentCategoryListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in PaymentCategory._meta.fields if True]


admin.site.register(PaymentCategory, PaymentCategoryListAdmin)


class ShopLocalityListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in ShopLocality._meta.fields if True]


admin.site.register(ShopLocality, ShopLocalityListAdmin)


class ShopListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Shop._meta.fields if True]


admin.site.register(Shop, ShopListAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in ProductCategory._meta.fields if True]


admin.site.register(ProductCategory, ProductCategoryAdmin)


class ProductListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Product._meta.fields if True]


admin.site.register(Product, ProductListAdmin)


class CustomerOrderListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in CustomerOrder._meta.fields if True]


admin.site.register(CustomerOrder, CustomerOrderListAdmin)


class DeliveryProfileListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in DeliveryProfile._meta.fields if True]


admin.site.register(DeliveryProfile, DeliveryProfileListAdmin)

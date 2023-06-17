from django.contrib import admin
from app_orders.models import Order, Payment

class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ["products"]
    list_display = [f.name for f in Order._meta.fields]


admin.site.register(Order, OrderAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Payment._meta.fields]


admin.site.register(Payment, PaymentAdmin)


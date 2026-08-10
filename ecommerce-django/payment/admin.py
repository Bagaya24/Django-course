from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.ShippingAddress)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)

#  Create an Order Item inline
class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    extra = 0

# Extend our Order Model
class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    readonly_fields = ["date_ordered"]
    inlines = [OrderItemInline]

# Unregister order Model
admin.site.unregister(models.Order)

# Re-register our order and order items
admin.site.register(models.Order, OrderAdmin)

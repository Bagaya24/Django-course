from django.contrib import admin
from django.contrib.auth.models import User
from . import models

# Register your models here.
admin.site.register(models.Categories)
admin.site.register(models.Customers)
admin.site.register(models.Products)
admin.site.register(models.Orders)
admin.site.register(models.Profile)

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = models.Profile

# Extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re-register the new way
admin.site.register(User, UserAdmin)
from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import APICallCounter

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "phone_number", "is_active", "date_joined")
    search_fields = ("username", "first_name", "last_name", "phone_number")

@admin.register(APICallCounter)
class APICallCounterAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "count")
    list_filter = ("date",)
    search_fields = ("user__username",)

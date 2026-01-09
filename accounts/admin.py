from django.contrib import admin
from .models import CustomUser

admin.site.register(CustomUser)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff')
    list_filter = ('role', 'is_approved', 'is_staff')
    search_fields = ('username', 'email')

# Register your models here.

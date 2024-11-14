from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phoneNum', 'birth')  # Use actual field names in CustomUser

admin.site.register(CustomUser, CustomUserAdmin)

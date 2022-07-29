from django.contrib import admin

# Register your models here.
from .models import *

# from .models import CustomUser

admin.site.register(League_Mod)
admin.site.register(User_Leagues)

# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ("username","first_name","last_name","email","leagues")

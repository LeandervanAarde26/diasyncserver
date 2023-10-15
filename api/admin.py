from django.contrib import admin
from .models import *
# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_display = ("first_name" , "last_name","sex", "diabetes_type")
admin.site.register(Users, UsersAdmin)

admin.site.register(GlucoseReading)

#Password@12
#Leander.vaonline@icloud.com -> L@v3nd3r
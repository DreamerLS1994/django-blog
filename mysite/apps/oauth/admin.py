from django.contrib import admin
from .models import Ouser


@admin.register(Ouser)
class OauthAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']



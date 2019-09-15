from django.contrib import admin
from .models import Tool
import xadmin
from xadmin import views
# Register your models here.


class ToolAdmin(object):
    model_icon = 'fa fa-gavel'


xadmin.site.register(Tool, ToolAdmin)


from django.contrib import admin
import xadmin
from xadmin import views
from .models import ArticleComment, Notification

# Register your models here.


class ArticleCommentAdmin(object):
    model_icon = 'fa fa-comments'


class NotificationAdmin(object):
    model_icon = 'fa fa-bell'


xadmin.site.register(ArticleComment, ArticleCommentAdmin)
xadmin.site.register(Notification, NotificationAdmin)


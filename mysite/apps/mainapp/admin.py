from django.contrib import admin
from .models import Carousel, Friendlink, Settings, Catalogue, Tag, Article, SiteAbout, Timeline
import xadmin
from xadmin import views

# Register your models here.


class GlobalSetting(object):
    # 设置后台顶部标题   
    site_title ='后台管理'
    # 设置后台底部标题   
    site_footer ='JerryCoding'


class BaseSetting(object):
    # 启用主题管理器   
    enable_themes = True
    # 使用主题   
    use_bootswatch = True


class CarouselAdmin(object):
    model_icon = 'fa fa-picture-o'


class FriendlinkAdmin(object):
    model_icon = 'fa fa-link'


class SettingsAdmin(object):
    model_icon = 'fa fa-cog'


class CatalogueAdmin(object):
    model_icon = 'fa fa-book'


class TagAdmin(object):
    model_icon = 'fa fa-tags'


class ArticleAdmin(object):
    list_filter = ('catalogue',)
    model_icon = 'fa fa-plane'
    # 搜索框
    search_fields = ('title',) 

class SiteAboutAdmin(object):
    model_icon = 'fa fa-flag'


class SiteTimelineAdmin(object):
    model_icon = 'fa fa-bug'


xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Catalogue, CatalogueAdmin)
xadmin.site.register(Tag, TagAdmin)

xadmin.site.register(Carousel, CarouselAdmin)
xadmin.site.register(Friendlink, FriendlinkAdmin)
xadmin.site.register(Settings, SettingsAdmin)

xadmin.site.register(SiteAbout, SiteAboutAdmin)
xadmin.site.register(Timeline, SiteTimelineAdmin)
# 注册主题设置
xadmin.site.register(views.BaseAdminView, BaseSetting)

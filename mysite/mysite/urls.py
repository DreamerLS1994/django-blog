"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static, serve
from django.contrib.sitemaps.views import sitemap
from mainapp.sitemaps import ArticleSitemap, CatalogueSitemap, TagSitemap, ToolSitemap
from mainapp.views import page_not_found, page_forbidden, page_error
from django.views.generic import TemplateView

import xadmin

sitemaps = {
    'articles': ArticleSitemap,
    'catalogues': CatalogueSitemap,
    'tags': TagSitemap,
    'tools': ToolSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('oauth.urls', namespace='oauth')),
    path('search/', include('haystack.urls')),  # 搜索路由
    path('', include('mainapp.urls', namespace='mainapp')),
    path('', include('tools.urls', namespace='tools')),
    path('static/', serve, {"document_root": settings.STATIC_ROOT}),
    path('media/', serve, {"document_root": settings.MEDIA_ROOT}),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('comment/', include('comment.urls', namespace='comment')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')), # robots

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件

# 全局403
#handler403 = page_forbidden

# 全局404
handler404 = page_not_found

# 全局500
handler500 = page_error

from django.urls import path
from .views import index_view, index_hot_view, article_detail_view, archives_view, \
    catalogue_detail_view, tag_detail_view, about_view, timeline_view, article_like_view
from .feeds import AllArticleRssFeed

app_name = '[mainapp]'

urlpatterns = [
    path('', index_view, name='index_url'),
    path('hot/', index_hot_view, name='index_hot_url'),
    path('about/', about_view, name='about_url'),
    path('timeline/', timeline_view, name='timeline_url'),
    path('archives/', archives_view, name='archives_url'),
    path('article/like', article_like_view, name='article_like_url'),
    path('article/<str:slug>/', article_detail_view, name='article_detail_url'),
    path('catalogue/<str:slug>/', catalogue_detail_view, name='catalogue_detail_url'),
    path('tag/<str:slug>/', tag_detail_view, name='tag_detail_url'),
    path('feed/', AllArticleRssFeed(), name='rss_url'),
]


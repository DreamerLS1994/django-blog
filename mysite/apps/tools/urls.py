from django.urls import path
from .views import tool_list_view, tool_detail_view, tool_like_view

app_name = '[tools]'

urlpatterns = [
    path('tools/', tool_list_view, name='tool_list_url'),
    path('tool/like', tool_like_view, name='tool_like_url'),
    path('tool/<str:slug>/', tool_detail_view, name='tool_detail_url'),
]


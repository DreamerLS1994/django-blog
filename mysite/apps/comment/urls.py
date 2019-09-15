from django.urls import path
from .views import cmt_add_view, noti_all_view, noti_unread_view, noti_markread_view, noti_delete_view

app_name = '[comment]'

urlpatterns = [
    path('add', cmt_add_view, name='cmt_add_url'),# 添加评论:
    path('notification/all/', noti_all_view, name='noti_all_url'),  # 显示所有哦消息:
    path('notification/unread/', noti_unread_view, name='noti_unread_url'),  # 显示所有未读消息:
    path('notification/markread', noti_markread_view, name='noti_markread_url'),  # 标记为已读:
    path('notification/delete', noti_delete_view, name='noti_delete_url'),  # 删除消息:

]


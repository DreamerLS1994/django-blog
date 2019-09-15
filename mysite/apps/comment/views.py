import time
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ArticleComment, Notification
from . import handlers
from mainapp.views import get_data
from mainapp.models import Article
# Create your views here.


@login_required
@require_POST
def cmt_add_view(request):
    if request.is_ajax():
        comment_user = request.user  # 获取评论的用户
        comment_articleid = request.POST.get('article_id')  # 获取评论的文章
        comment_body = request.POST.get('body')  # 获取评论的内容
        comment_parent_id = request.POST.get('parent_id')
        comment_rep_id = request.POST.get('rep_to_id')

        # 每次评论间隔需要大于60s
        key = "cmt_time_{}_{}".format(comment_user.id, comment_articleid)
        last_cmt_time = request.session.get(key)

        # 如果有这个key 并且间隔小于60s
        if last_cmt_time:
            now_time = time.time()
            t = now_time - last_cmt_time
            if t < 60:
                return JsonResponse({'msg': '评论频率过快！'})

        request.session[key] = time.time()
        article = Article.objects.get(id=comment_articleid)  # 获取评论的文章
        if comment_parent_id == None:
            comment_parent = None
        else:
            comment_parent = ArticleComment.objects.get(id=comment_parent_id)

        if comment_rep_id == None:
            comment_rep = None
        else:
            comment_rep = ArticleComment.objects.get(id=comment_rep_id)

        comment = ArticleComment(owner=comment_user, body=comment_body, belong=article, parent=comment_parent,
                                 rep_to=comment_rep)  # 创建一个新的comment

        comment.save()  # 保存数据

        new_cmt_id = '#cmt-'+str(comment.id)  # 获取新添加的comment.id  用于返回Jason
        return JsonResponse({'msg': '评论提交成功！', 'new_cmt_id': new_cmt_id})
    return JsonResponse({'msg': '评论提交失败！'})


@login_required
def noti_all_view(request):
    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext = get_data()
    notifications = request.user.get_all_notis()

    return render(request, 'comment/notis.html', {'carousels': g_carousels, 'friendlinks': g_friendlinks,
                                                  'settings': g_settings,'catalogues': g_catalogues,
                                                  'tags': g_tags, 'notis': notifications, 'one': g_onetext})


@login_required
def noti_unread_view(request):
    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext= get_data()
    notifications = request.user.get_unread_notis()

    return render(request, 'comment/notis.html', {'carousels': g_carousels, 'friendlinks': g_friendlinks,
                                                  'settings': g_settings,'catalogues': g_catalogues,
                                                  'tags': g_tags, 'notis': notifications, 'one': g_onetext})


@login_required
@require_POST
def noti_markread_view(request):
    if request.is_ajax():
        noti_id = request.POST.get('noti_id')
        noti = get_object_or_404(Notification, id=noti_id)
        noti.mark_to_read()
        print("mark success")
        return JsonResponse({'msg': '标记已读成功！'})
    return JsonResponse({'msg': '标记失败！'})


@require_POST
@login_required
def noti_delete_view(request):
    if request.is_ajax():
        noti_id = request.POST.get('noti_id')
        noti = get_object_or_404(Notification, id=noti_id)
        noti.delete()

        return JsonResponse({'msg': '删除成功！'})
    return JsonResponse({'msg': '删除失败！'})


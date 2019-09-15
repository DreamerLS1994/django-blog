from django.shortcuts import render
from tools.models import Tool
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from mainapp.views import get_data, get_random
import time
# Create your views here.


def tool_list_view(request):
    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext = get_data()
    g_randoms = get_random()

    tools = Tool.objects.all()
    return render(request, 'tools/tool_list.html', {'carousels': g_carousels, 'friendlinks': g_friendlinks,
                                                    'settings': g_settings,'catalogues': g_catalogues,
                                                    'tags': g_tags, 'tools': tools, 'one': g_onetext, 'randoms': g_randoms})


def tool_detail_view(request, slug):
    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext = get_data()
    g_randoms = get_random()
    tool = get_object_or_404(Tool, slug=slug)

    key = "read_tool_time{}".format(tool.id)
    last_read_time = request.session.get(key)

    # 第一次阅读或者阅读超过1小时 阅览+1
    if not last_read_time:
        tool.add_readings()
        request.session[key] = time.time()
    else:
        now_time = time.time()
        t = now_time - last_read_time
        if t > 60 * 60:
            tool.add_readings()
            request.session[key] = time.time()

    return render(request, 'tools/tool_detail.html', {'carousels': g_carousels, 'friendlinks': g_friendlinks,
                                                    'settings': g_settings,'catalogues': g_catalogues,
                                                    'tags': g_tags, 'this_tool': tool, 'one': g_onetext, 'randoms': g_randoms})


@require_POST
def tool_like_view(request):
    if request.is_ajax():
        this_toolid = request.POST.get('this_toolid')
        print(this_toolid)
        this_tool = get_object_or_404(Tool, id=this_toolid)

        this_tool.add_likes()

    return JsonResponse({'msg': '点赞失败！'})

import time
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from .models import Carousel, Friendlink, Settings, Catalogue, Tag, Article, SiteAbout, Timeline
from comment.models import ArticleComment
from itertools import chain

def page_forbidden(request, exception):
    response = render_to_response("403.html", {})
    response.status_code = 403
    return response

def page_not_found(request, exception):
    response = render_to_response("mainapp/404.html", {})
    response.status_code = 404
    return response

def page_error(exception):
    response = render_to_response("mainapp/500.html", {})
    response.status_code = 500
    return response


def get_random():
    # 随机推荐 文章获取 12 篇
    randoms = Article.objects.order_by('?')[:12]
    return randoms


def get_data():
    carousels = Carousel.objects.all()
    settings = Settings.objects.first()
    catalogues = Catalogue.objects.all()
    tags = Tag.objects.all()
    friendlinks = Friendlink.objects.filter(is_show=True)

    one_text = '但愿人长久，千里共婵娟。'

    return carousels, settings, catalogues, tags, friendlinks, one_text


def index_view(request):
    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext = get_data()
    g_randoms = get_random()

    articles = Article.objects.filter(is_draft=False, is_top=False)
    articles_top = Article.objects.filter(is_draft=False, is_top=True)

    # 拼接置顶文章和普通文章
    g_articles = list(chain(articles_top, articles))

    # NUM_PER_PAGE篇文章一页，最后一页1篇文章时，合并到上一页
    paginator = Paginator(g_articles, settings.NUM_PER_PAGE, 1)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except InvalidPage:
        raise Http404("none")
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'mainapp/index.html',
                  {'carousels': g_carousels, 'friendlinks': g_friendlinks, 'settings': g_settings,
                   'catalogues': g_catalogues, 'tags': g_tags, 'articles': articles, 'one': g_onetext, 'randoms': g_randoms})


def index_hot_view(request):
    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext = get_data()
    g_randoms = get_random()
    articles_top = Article.objects.filter(is_draft=False, is_top=True)
    articles = Article.objects.filter(is_draft=False, is_top=False).order_by('-readings')

    # 拼接置顶文章和普通文章
    g_articles = list(chain(articles_top, articles))

    # NUM_PER_PAGE篇文章一页，最后一页1篇文章时，合并到上一页
    paginator = Paginator(g_articles, settings.NUM_PER_PAGE, 1)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except InvalidPage:
        raise Http404("none")
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'mainapp/index.html',
                  {'carousels': g_carousels, 'friendlinks': g_friendlinks, 'settings': g_settings,
                   'catalogues': g_catalogues, 'tags': g_tags, 'articles': articles, 'one': g_onetext, 'randoms': g_randoms})


def article_detail_view(request, slug):
    # 获取侧栏等数据
    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext= get_data()
    g_randoms = get_random()

    # 寻找所有发表文章
    articles = Article.objects.filter(is_draft=False)
    this_article = get_object_or_404(articles, slug=slug)

    # 找到这篇文章的 所有 的 评论
    g_comments = ArticleComment.objects.filter(belong=this_article)
    this_tags = this_article.tag.all()
    key = "read_time_{}".format(this_article.id)
    last_read_time = request.session.get(key)

    # 第一次阅读或者阅读超过1小时 阅览+1 除了作者外
    if request.user != this_article.author:
        if not last_read_time:
            this_article.add_readings()
            request.session[key] = time.time()
        else:
            now_time = time.time()
            t = now_time - last_read_time
            if t > 60 * 60:
                this_article.add_readings()
                request.session[key] = time.time()

    return render(request, 'mainapp/article_detail.html',
                  {'carousels': g_carousels, 'friendlinks': g_friendlinks, 'settings': g_settings,
                   'catalogues': g_catalogues, 'tags': g_tags,
                   'this_article': this_article,  'tag_list': this_tags,
                   'comments': g_comments, 'one': g_onetext, 'randoms': g_randoms})


def catalogue_detail_view(request, slug):
    # 获取侧栏等数据
    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext = get_data()
    g_randoms = get_random()    

    # 找到该目录
    this_catalogue = get_object_or_404(Catalogue, slug=slug)

    # 找到属于该目录的所有非草稿文章
    articles_top = Article.objects.filter(catalogue=this_catalogue, is_draft=False, is_top=True)
    articles = Article.objects.filter(catalogue=this_catalogue, is_draft=False, is_top=False)
    # 拼接置顶文章和普通文章
    g_articles = list(chain(articles_top, articles))

    # NUM_PER_PAGE篇文章一页，最后一页1篇文章时，合并到上一页
    paginator = Paginator(g_articles, settings.NUM_PER_PAGE, 1)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except InvalidPage:
        raise Http404("none")
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'mainapp/catalogue_detail.html',
                  {'carousels': g_carousels, 'friendlinks': g_friendlinks, 'settings': g_settings,
                   'catalogues': g_catalogues, 'tags': g_tags, 'articles': articles,
                   'this_catalogue': this_catalogue, 'one': g_onetext, 'randoms': g_randoms})


def tag_detail_view(request, slug):
    # 获取侧栏等数据
    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext = get_data()
    g_randoms = get_random()
    # 找到该目录
    this_tag = get_object_or_404(Tag, slug=slug)
    # 找到属于该目录的所有非草稿文章
    articles_top = Article.objects.filter(tag=this_tag, is_draft=False, is_top=True)
    articles = Article.objects.filter(tag=this_tag, is_draft=False, is_top=False)

    # 拼接置顶文章和普通文章
    g_articles = list(chain(articles_top, articles))

    # NUM_PER_PAGE篇文章一页，最后一页1篇文章时，合并到上一页
    paginator = Paginator(g_articles, settings.NUM_PER_PAGE, 1)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except InvalidPage:
        raise Http404("none")
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'mainapp/tag_detail.html',
                  {'carousels': g_carousels, 'friendlinks': g_friendlinks, 'settings': g_settings,
                   'catalogues': g_catalogues, 'tags': g_tags, 'articles': articles,
                   'this_tag': this_tag, 'one': g_onetext, 'randoms': g_randoms})


def about_view(request):
    # 获取侧栏等数据
    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext = get_data()
    g_randoms = get_random()
    g_abouts = SiteAbout.objects.all()

    return render(request, 'mainapp/about.html',
                  {'carousels': g_carousels, 'friendlinks': g_friendlinks, 'settings': g_settings,
                   'catalogues': g_catalogues, 'tags': g_tags, 'abouts': g_abouts, 'one': g_onetext, 'randoms': g_randoms})


def timeline_view(request):
    # 获取侧栏等数据
    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext = get_data()
    g_randoms = get_random()

    g_timelines = Timeline.objects.all()

    return render(request, 'mainapp/timeline.html',
                  {'carousels': g_carousels, 'friendlinks': g_friendlinks, 'settings': g_settings,
                   'catalogues': g_catalogues, 'tags': g_tags, 'timelines': g_timelines, 'one': g_onetext, 'randoms': g_randoms})


def archives_view(request):
    # 获取侧栏等数据
    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext = get_data()
    g_randoms = get_random()
    g_articles = Article.objects.filter(is_draft=False)

    g_dates = Article.objects.distinct_date

    return render(request, 'mainapp/archives.html',
                  {'carousels': g_carousels, 'friendlinks': g_friendlinks, 'settings': g_settings,
                   'catalogues': g_catalogues, 'tags': g_tags, 'articles': g_articles, 'dates': g_dates, 'one': g_onetext, 'randoms': g_randoms})


@require_POST
def article_like_view(request):
    if request.is_ajax():
        this_articleid = request.POST.get('this_articleid')
        this_article = get_object_or_404(Article, id=this_articleid)
        # 获取上次点赞的时间，一小时内只可以点赞一次
        key = "like_time_{}".format(this_article.id)
        last_like_time = request.session.get(key)

        this_article.add_likes()
        # 第一次点赞或者超过1小时 like+1 除了作者外

        '''
        if request.user != this_article.author:
            if not last_like_time:
                this_article.add_likes()
                request.session[key] = time.time()
            else:
                now_time = time.time()
                t = now_time - last_like_time
                if t > 60 * 60:
                    this_article.add_likes()
                    request.session[key] = time.time()
                else:
                    return JsonResponse({'msg': '您已点赞！'})

        return JsonResponse({'msg': '点赞成功！'})
        '''
    return JsonResponse({'msg': '点赞失败！'})

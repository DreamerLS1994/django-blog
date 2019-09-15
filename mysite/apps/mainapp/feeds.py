from django.contrib.syndication.views import Feed
from django.shortcuts import reverse
from .models import Article, Settings


class AllArticleRssFeed(Feed):
    my_setting = Settings.objects.first()
    if my_setting is not  None:
        # 显示在聚会阅读器上的标题
        title = my_setting.title
        # 跳转网址，为主页
        link = "/"
        # 描述内容
        description = my_setting.desc

    # 需要显示的内容条目，这个可以自己挑选一些热门或者最新的博客
    def items(self):
        return Article.objects.all()[:50]

    # 显示的内容的标题,这个才是最主要的东西
    def item_title(self, item):
        return "【{}】{}".format(item.catalogue, item.title)

    # 显示的内容的描述
    def item_description(self, item):
        return item.summary + item.body[:100]

    def item_link(self, item):
        return reverse('mainapp:article_detail_url', kwargs={'slug': item.slug})


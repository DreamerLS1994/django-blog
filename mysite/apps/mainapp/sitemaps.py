from django.contrib.sitemaps import Sitemap
from .models import Article, Catalogue, Tag
from tools.models import Tool


class ArticleSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.update_date


class CatalogueSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Catalogue.objects.all()

    def lastmod(self, obj):
        return obj.article_set.first().create_date


class TagSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Tag.objects.all()

    def lastmod(self, obj):
        return obj.article_tags.first().update_date


class ToolSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return Tool.objects.all()

    def lastmod(self, obj):
        return obj.create_date


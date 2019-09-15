from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField
from comment.models import ArticleComment
# Create your models here.

# 图片轮播
class Carousel(models.Model):
    number = models.IntegerField('编号', help_text='编号决定图片播放的顺序，图片不要多于4张')
    title = models.CharField('标题', max_length=20, blank=True)
    content = models.CharField('描述', max_length=80, blank=True, help_text='内容可以为空')
    img_url = ProcessedImageField(upload_to='carousel',
                                  default='carousel/default.jpg',
                                  blank=True,
                                  verbose_name='轮播图片',
                                  # 图片将处理成900x450的尺寸
                                  processors=[ResizeToFill(900, 450)],
                                  help_text='图片将被拉伸成900x450尺寸')
    url = models.URLField('跳转链接', max_length=150, blank=True, help_text='图片跳转的超链接')

    class Meta:
        verbose_name = '图片轮播'
        verbose_name_plural = verbose_name
        # 编号越小越靠前，添加的时间约晚约靠前
        ordering = ['number', '-id']

    def __str__(self):
        return self.title


# 网站友链
class Friendlink(models.Model):
    number = models.IntegerField('编号', help_text='编号决定友链的顺序，越小越靠前')
    name = models.CharField('友链名称', max_length=20, help_text='友链名称，展示在网页上的链接名称')
    summary = models.CharField('友链介绍', max_length=80, help_text='友链介绍，鼠标悬停显示')
    url = models.URLField('友链链接', max_length=80, help_text='友链链接(格式：http://xxxxx)，用于跳转')
    is_show = models.BooleanField('主页展示', default=True, help_text='选中表明展示')

    class Meta:
        verbose_name = '网站友链'
        verbose_name_plural = verbose_name  # 复数形式
        ordering = ['number']  # 越小越靠前

    def __str__(self):
        return self.name[:20]


# 本站说明
class SiteAbout(models.Model):
    number = models.IntegerField('位置顺序', help_text='编号决定关于模块的顺序，越小越靠前')
    name = models.CharField('标题', max_length=20, help_text='例如：关于xxx')
    body = RichTextUploadingField(config_name='my_config', verbose_name='内容', help_text='输入关于xxx的内容....')

    class Meta:
        verbose_name = '关于本站'
        verbose_name_plural = verbose_name
        # 编号越小越靠前，添加的时间约晚约靠前
        ordering = ['number', '-id']

    def __str__(self):
        return self.name


# 时间轴
class Timeline(models.Model):
    name = models.CharField('标题', max_length=20, help_text='事件标题..')
    body = RichTextUploadingField(config_name='my_config', verbose_name='事件内容', help_text='输入事件内容....')
    time = models.DateField('事件时间', help_text='请选择事件时间....')

    class Meta:
        verbose_name = '更新时间轴'
        verbose_name_plural = verbose_name
        # 编号越小越靠前，添加的时间约晚约靠前
        ordering = ['id']

    def __str__(self):
        return self.name


# 网站一般设置
class Settings(models.Model):
    title = models.CharField('网站名称', max_length=50, default="我的博客", help_text='网站名称，展示在网页上的名称')
    keywords = models.CharField('网站关键字', max_length=100, blank=True, help_text='网站关键字，用于网页元描述')
    desc = models.CharField('网站元描述', max_length=200, blank=True, help_text='网站元描述，用于网页元描述')

    brand_img = ProcessedImageField(upload_to='brand',
                                    default='brand/default.png',
                                    blank=True,
                                    verbose_name='导航栏商标图片',
                                    processors=[ResizeToFill(600, 200)],
                                    help_text='图片将被拉伸成600x200尺寸。')

    favicon_img = ProcessedImageField(upload_to='favicon',
                                      default='favicon/favicon.ico',
                                      blank=True,
                                      verbose_name='网站图标',
                                      processors=[ResizeToFill(32, 32)],
                                      help_text='需为ico格式图标，图标将被拉伸成32x32尺寸。')

    blog_news = models.CharField('博客动态', max_length=300, default='', blank=True, help_text='博客动态信息，最大字符数300')

    # 设置微信二维码用于展示
    wx_qr = ProcessedImageField(upload_to='contact',
                                default='contact/default.png',
                                verbose_name='联系二维码',
                                blank=True,
                                # 图片将处理成400x400的尺寸
                                processors=[ResizeToFill(400, 400)],
                                help_text='网站联系方式，图片将被拉伸成400x400尺寸')

    mail_url = models.CharField('联系邮箱', max_length=80, default='mailto:', blank=True, help_text='网站联系邮箱跳转链接')
    qq_url = models.CharField('QQ跳转链接', max_length=150, blank=True,
                              help_text='网站联系QQ链接，用于跳转, 如：tencent://message/?Site=baidu.com&uin=xxxxx&Menu=yes')
    github_url = models.URLField('GitHub链接', max_length=150, blank=True, help_text='GitHub链接，用于跳转')
    is_award = models.BooleanField('开启打赏', help_text='选中表明开启')  # default=True
    award_wximg = ProcessedImageField(upload_to='award',
                                      # default='award/default.png',
                                      verbose_name='微信打赏二维码',
                                      blank=True,
                                      # 图片将处理成400x400的尺寸
                                      processors=[ResizeToFill(400, 400)],
                                      help_text='微信打赏二维码，图片将被拉伸成400x400尺寸')

    award_aliimg = ProcessedImageField(upload_to='award',
                                       # default='award/default.png',
                                       verbose_name='支付宝打赏二维码',
                                       blank=True,
                                       # 图片将处理成400x400的尺寸
                                       processors=[ResizeToFill(400, 400)],
                                       help_text='支付宝打赏二维码，图片将被拉伸成400x400尺寸')
    class Meta:
        verbose_name = '网站设置'
        verbose_name_plural = verbose_name  # 复数形式

    def __str__(self):
        return '网站基本设置（只读一条）'


# 文章归档管理器
class ArticleManager(models.Manager):
    # 该管理器定义了一个distinct_date方法，目的是找出所有的不同日期
    def distinct_date(self):
        distinct_date_list = []  # 建立一个列表用来存放不同的日期 年-月
        date_list = self.values('create_date')  # 根据文章字段date_publish找出所有文章的发布时间
        for date in date_list:  # 对所有日期进行遍历，当然这里会有许多日期是重复的，目的就是找出多少种日期
            date = date['create_date'].strftime('%Y-%m') # 取出一个日期改格式为 ‘xxx年/xxx月 存档’
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list


# 文章分类
class Catalogue(models.Model):
    name = models.CharField('分类名称', max_length=20, help_text='文章分类名称，最多20字符')
    slug = models.SlugField('slug(请修改)', unique=True, help_text='唯一分类标识，推荐格式 hello-world')
    summary = models.TextField('分类摘要', max_length=300, help_text='文章分类的摘要介绍，最多300字符')

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    # 获取该目录下文章个数
    def get_articlecount(self):
        return Article.objects.filter(catalogue=self, is_draft=False).count()

    def get_absolute_url(self):
            return reverse('mainapp:catalogue_detail_url', kwargs={'slug': self.slug})


# 文章标签
class Tag(models.Model):
    name = models.CharField('标签名称', max_length=20, help_text='文章标签名称，最多20字符')
    slug = models.SlugField('slug(请修改)', unique=True, help_text='唯一标签标识，推荐格式 hello-world')
    summary = models.TextField('标签介绍', max_length=300, help_text='文章标签的摘要介绍，最多300字符')

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    # 获取该标签下文章个数
    def get_articlecount(self):
        return Article.objects.filter(tag=self, is_draft=False).count()

    def get_absolute_url(self):
        return reverse('mainapp:tag_detail_url', kwargs={'slug': self.slug})


# 文章主体
class Article(models.Model):
    title = models.CharField('文章标题', max_length=150, help_text='文章标题，最多150个字符')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='文章作者', )
    keywords = models.CharField('文章关键词', max_length=150, help_text='文章关键字，用于网页keyword元素')
    summary = models.TextField('文章摘要', max_length=300, help_text='文章摘要，最多300字符')
    create_date = models.DateTimeField('文章创建时间', auto_now_add=True)
    update_date = models.DateTimeField('文章最后修改时间', auto_now=True)
    body = RichTextUploadingField(config_name='my_config', verbose_name='内容', help_text='CKEditor集成富文本文章内容')

    img = ProcessedImageField(upload_to='article',
                              default='article/default.png',
                              blank='True',
                              verbose_name='文章封面图',
                              processors=[ResizeToFill(450, 300)],
                              help_text='文章封面图将被拉伸成450x300尺寸')

    slug = models.SlugField('slug(唯一性)', unique=True, max_length=40, default='', help_text='唯一标签标识，推荐格式 hello-world')
    catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE, verbose_name='文章分类', help_text='选择文章的分类')
    tag = models.ManyToManyField(Tag, related_name='article_tags', blank=True, verbose_name='文章标签', help_text='选择文章的标签')

    readings = models.IntegerField('阅览量', default=0)
    like_num = models.IntegerField('点赞量', default=0)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                  related_name='like_user',
                                  verbose_name='点赞者',
                                  blank=True, help_text='点赞该文章的用户')

    is_draft = models.BooleanField('是否存为草稿', default=False, help_text='勾选则存为草稿，主页不显示')
    is_top = models.BooleanField('是否置顶', default=False, help_text='勾选则置顶')
    is_comment = models.BooleanField('是否可以评论', default=True, help_text='勾选则可以评论')

    objects = ArticleManager()

    class Meta:
        verbose_name = '文章发表'  # 通俗易懂的名字
        verbose_name_plural = verbose_name  # 复数形式
        ordering = ['-create_date']  # 降序排序

    def __str__(self):
        return self.title[:20]

    # 阅读量计数增加
    def add_readings(self):
        self.readings += 1
        self.save(update_fields=['readings'])

    # 点赞量计数增加
    def add_likes(self):
        self.like_num += 1
        self.save(update_fields=['like_num'])

    # 获取评论数
    def get_comment_count(self):
        return ArticleComment.objects.filter(belong=self).count()

    # 获取评论参与人数
    def get_commenter_count(self):
        comments = ArticleComment.objects.filter(belong=self)
        owners = []
        for i in comments:
            owners.append(i.owner)

        return len(set(owners))

    # 获取上一篇
    def get_pre(self):
        article = Article.objects.filter(id__lt=self.id).order_by('-create_date').first()
        if article is None:
            return None
        while article.is_draft is True:
            a = article
            article = Article.objects.filter(id__lt=a.id).order_by('-create_date').first()
            if article is None:
                return None
        return article

    # 获取下一篇
    def get_next(self):
        article = Article.objects.filter(id__gt=self.id).order_by('create_date').first()
        if article is None:
            return None
        while article.is_draft is True:
            tmp = article
            article = Article.objects.filter(id__gt=tmp.id).order_by('create_date').first()
            if article is None:
                return None
        return article

    # 获取文章url
    def get_url(self):
        return reverse('mainapp:article_detail_url', kwargs={'slug': self.slug})

    def get_absolute_url(self):
            return reverse('mainapp:article_detail_url', kwargs={'slug': self.slug})


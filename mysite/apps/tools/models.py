from django.db import models
from django.shortcuts import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Tool(models.Model):
    name = models.CharField(max_length=50, verbose_name='工具名称', help_text="请输入工具名称，建议12个字以内。")
    summary = models.TextField('工具介绍', max_length=100, help_text='请输入工具介绍，不建议过长。')
    body = RichTextUploadingField(config_name='my_config', verbose_name='工具详情', help_text='描述工具使用详情。')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    img_link = ProcessedImageField(upload_to='tools',
                                   default='',
                                   blank=True,
                                   verbose_name='工具图标',
                                   # 图片将处理成400x400的尺寸
                                   processors=[ResizeToFill(400, 400)],
                                   help_text='图片将被拉伸成400x400尺寸')

    readings = models.IntegerField('阅览量', default=0)
    likes = models.IntegerField('点赞量', default=0)

    slug = models.SlugField('slug(请修改)', unique=True, help_text='唯一分类标识，推荐格式 hello-world')

    class Meta:
        verbose_name = '在线工具'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.name

    # 阅读量计数增加
    def add_readings(self):
        self.readings += 1
        self.save(update_fields=['readings'])

    # 点赞量计数增加
    def add_likes(self):
        self.likes += 1
        self.save(update_fields=['likes'])

    def get_absolute_url(self):
        return reverse('tools:tool_detail_url', kwargs={'slug': self.slug})


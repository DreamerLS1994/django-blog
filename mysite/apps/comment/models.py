from django.db import models
from django.conf import settings

# Create your models here.


class Comment(models.Model):
    cmt_id = models.CharField('评论id', max_length=20, blank=True, help_text='自动生成，用户段落的快速跳转')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='评论人')
    body = models.TextField('评论内容', max_length=settings.COMMENT_MAX_LENGTH)
    create_date = models.DateTimeField('评论时间', auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='父评论',
                               related_name='child_comments', blank=True, null=True)
    rep_to = models.ForeignKey('self',  on_delete=models.CASCADE, verbose_name='回复',
                               related_name='rep_comments', blank=True, null=True)

    class Meta:
        # 这是一个元类，用来继承的
        abstract = True

    def __str__(self):
        return self.body[:20]


class ArticleComment(Comment):
    belong = models.ForeignKey(settings.ARTICLE_MODEL, on_delete=models.CASCADE,
                               related_name='articles_comments', verbose_name='所属文章')

    class Meta:
        verbose_name = '文章评论'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    # 判断是否是父评论
    def is_parent(self):
        # 没有父评论 他就是父评论
        if self.parent is None:
            return True
        return False

    def get_child_comment(self):
        return self.child_comments.all().order_by('create_date')

    def __str__(self):
        return '文章评论{}'.format(self.id)


class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='消息发送者',
                               related_name='notification_sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='消息接收者',
                                 related_name='notification_receiver')
    belong = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, verbose_name='消息所属评论',
                               related_name='comment')
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    is_read = models.BooleanField('是否已读', default=False, help_text='是否标记为已读，勾选为已读')

    def mark_to_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])

    class Meta:
        verbose_name = '消息通知'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return '{}回复了{}'.format(self.sender, self.receiver)

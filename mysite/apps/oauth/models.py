from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from comment.models import Notification

# Create your models here.

class Ouser(AbstractUser):
    avatar = ProcessedImageField(upload_to='avatar/%Y/%m/%d',
                                 default='avatar/default.jpg',
                                 blank=True,
                                 verbose_name='头像',
                                 # 图片将处理成100x100的尺寸
                                 processors=[ResizeToFill(100, 100)], )

    signature = models.CharField(max_length=100, blank=True, default='大家好~', verbose_name="签名")

    def __str__(self):
        return self.username

    def get_all_notis(self):
        # 找到这用户的 所有 的 消息
        notifications = Notification.objects.filter(receiver=self)
        return notifications

    def get_unread_notis(self):
        notifications = Notification.objects.filter(receiver=self, is_read=False)
        return notifications


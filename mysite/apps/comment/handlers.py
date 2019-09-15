from .models import ArticleComment, Notification
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


def notify_handler(sender, instance, created, **kwargs):
    article = instance.belong
    sender = instance.owner

    # 设置邮件参数
    email_subject = '[Jerry Coding] 您的评论收到了新回复'
    arti_url = reverse('mainapp:article_detail_url', args=(instance.belong.slug,))
    email_message = '您好,\n\n您在 JerryCoding 《' + instance.belong.title + '》的评论有了新回复！快来点击下面链接看看吧！\nhttps://www.jerrycoding.com' + arti_url + '\n\nwww.jerrycoding.com'
    email_sender = settings.DEFAULT_FROM_EMAIL
    email_receiver = []

    if created:
        if instance.rep_to:
            receiver = instance.rep_to.owner
            if receiver == article.author:  # 二级评论被回复者就是作者，只通知一次
                new_notify = Notification(sender=sender, receiver=receiver, belong=instance)
                new_notify.save()
            else:  # 二级评论作者和被回复者不是一人
                receiver2 = article.author  # 通知作者
                if sender != receiver2:
                    new_notify = Notification(sender=sender, receiver=receiver2, belong=instance)
                    new_notify.save()
                receiver3 = instance.rep_to.owner  # 通知回复者
                if sender != receiver3:
                    new_notify = Notification(sender=sender, receiver=receiver3, belong=instance)
                    new_notify.save()
            # 发送邮件通知
            email_receiver.append(receiver.email)
            send_mail(email_subject, email_message, email_sender, email_receiver, fail_silently=True)
        else:
            if instance.parent:  # 不是回复评论，是评论了评论
                receiver2 = article.author  # 告知作者
                if sender != receiver2:
                    new_notify = Notification(sender=sender, receiver=receiver2, belong=instance)
                    new_notify.save()
                receiver3 = instance.parent.owner  # 告知被评论者
                if sender != receiver3:
                    new_notify = Notification(sender=sender, receiver=receiver3, belong=instance)
                    new_notify.save()

                email_receiver.append(instance.parent.owner.email)

            else:
                receiver = article.author
                if sender != receiver:
                    new_notify = Notification(sender=sender, receiver=receiver, belong=instance)
                    new_notify.save()
                email_receiver.append(receiver.email)

            # 发送邮件通知
            send_mail(email_subject, email_message, email_sender, email_receiver, fail_silently=True)


post_save.connect(notify_handler, sender=ArticleComment)

from django.db.models.signals import m2m_changed, post_save
from django.template.loader import render_to_string
from django.conf import settings
from .models import PostCategory, Post
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .tasks import task_about_new_post

#запускаем сигнал таске ( task_about_new_post().delay() ) на отправку письма о новом посте подписантам категории
@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all() # в PostCategory поле наз-ся category, но тут он ищет это поле в модели Post-post_category
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]  #список почт подписчиков
        task_about_new_post.delay(instance.preview(), instance.pk, instance.title, subscribers_emails)


#instance.title, instance.text, instance.date_in, instance.news_or_article, instance.post_category
#'author', 'title', 'text', 'post_category'

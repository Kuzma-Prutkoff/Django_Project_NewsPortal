from celery import shared_task
from .models import Post, Category
from datetime import datetime, timedelta
import datetime
import logging
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


logger = logging.getLogger(__name__)
@shared_task
def task_new_posts_7d(): #задача на отправку постов за неделю подписчикам запускается в селери по пн-8:00
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_in__gte=last_week) # посты больше или = чем неделя отроду
    categories = set(posts.values_list('post_category__name_category', flat=True)) # множество, чтобы не дублировались,
    #flat=True если без него, то в пьсьме придет словарь типа {категория:текст},а так придет только текст поста. плоский список, без словарей
    subscribers = set(Category.objects.filter(name_category__in=categories).values_list('subscribers__email', flat=True)) #
    html_content = render_to_string(
        'weekly_post.html', {'link': settings.SITE_URL, 'posts': posts}
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='', # у нас шаблон weekly_post.html, там все напишем
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def task_about_new_post(preview, pk, title, subscribers):  # задача на отправку сообщения о новом посте для подписчика
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/post/{pk}' #   http://127.0.0.1:8000/post/pk
        }
    )
    msg = EmailMultiAlternatives(subject=title, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

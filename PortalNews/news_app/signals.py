from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from django.conf import settings
from .models import PostCategory
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives


def send_notification(preview, pk, title, subscribers):  # отдельно делаем функцию отправки сообщения о новом посте для подписчика
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

@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all() # в PostCategory поле наз-ся category, но тут он ищет это поле в модели Post-post_category
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]  #список почт подписчиков
        send_notification(instance.preview(), instance.pk, instance.title, subscribers_emails)  #


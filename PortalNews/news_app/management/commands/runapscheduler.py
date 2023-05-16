import datetime
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news_app.models import Post, Category          #  подчеркнуто красным но работает
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)
def my_job():
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
        body='', # у нас шаблон будет, там все напишем
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(my_job, trigger=CronTrigger(day_of_week=4, hour="18", minute="00"), # рассылка каждую пт в 18
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1, replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"), # по понедельникам шедулер будет удалять старые - delete_old_job_executions
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
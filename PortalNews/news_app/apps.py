from django.apps import AppConfig

class NewsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_app'
    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов. Из вебинара import news_app.signals
#                                  # и в сеттинге заменить news_app на INSTALLED_APPS = [news_app.apps.NewsConfig
#
#

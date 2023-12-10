from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from news_app import views

router = routers.DefaultRouter() # DjRestFramework
router.register(r'news', views.NewsViewset)
# router.register(r'articles', views.ArticlesViewset)
router.register(r'category', views.CategoryViewset)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')), # подключаем встроенные эндпоинты для работы с локализацией(языки сайта)
    path('admin/', admin.site.urls),
    path('post/', include('news_app.urls')),
    path("accounts/", include("allauth.urls")), #теперь можно логиниться через яндекс
    path('swagger-ui/', TemplateView.as_view(template_name='swagger-ui.html', extra_context={'schema_url': 'openapi-schema'}), name='swagger-ui'),
    path('api/', include(router.urls)), # DjRestFramework
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')) # DjRestFramework /login /logout
]

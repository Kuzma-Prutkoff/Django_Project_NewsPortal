from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', include('news_app.urls')),
    path("accounts/", include("allauth.urls")), #теперь можно логиниться через яндекс

]

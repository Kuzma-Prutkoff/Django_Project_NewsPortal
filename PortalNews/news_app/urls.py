from django.urls import path
from .views import NewsList, NewsDetail  # Импортируем созданное нами представление

urlpatterns = [
   path('', NewsList.as_view()),
   path('<int:pk>', NewsDetail.as_view()),
]

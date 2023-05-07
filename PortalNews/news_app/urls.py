from django.urls import path
from .views import (NewsList, NewsDetail, PostSearch, NewsCreate, PostUpdate, PostDelete,
                    ArticleCreate, CategoryListView, subscribe, unsubscribe)

urlpatterns = [
   path('', NewsList.as_view(), name='news_list'),
   path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticleCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_update'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'), # name='category_list' используем в шаблоне category_list
   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'), # куда попадем после подписки (Вы успешно подписались....)
   path('categories/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'), # куда попадем после отписки (Вы успешно отписались....)

]
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum  # for aggregate суммирование рейтинга методом Sum
from django.urls import reverse
from django.core.cache import cache
from django.utils.translation import gettext as _ # геттекст

class Author(models.Model):
    author_rating = models.IntegerField(default=0)
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta: # меняем в админке названия моделей на удобоваримый
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('post_rating'))  # берем модель post в ней суммируем поле post_rating
        pRat = 0
        pRat += postRat.get('postRating') # получаем это значение суммы

        commentRat = self.author_user.comment_set.aggregate(commentRating=Sum('comment_rating'))  # связь идет через User, поэтому .author_user.
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.author_rating = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=64, help_text=_('category name'), unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories') # делаем подписку

    def __str__(self): # теперь в БД во вкладке http://127.0.0.1:8000/admin/news_app/post/ названия категорий на понятном языке
        return self.name_category

    class Meta: # меняем в админке названия моделей на удобоваримый ru
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    N_or_A = [(NEWS, 'Новость'), (ARTICLE, 'Статья')]

    title = models.CharField(max_length=128)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    news_or_article = models.CharField(max_length=2, choices=N_or_A, default=NEWS)
    date_in = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    text = models.TextField(default="Текст отсутствует")
    post_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()
    def dislike(self):
         self.post_rating -= 1
         self.save()
    def preview(self):
        return f'{self.text[0:123]}...'
    def __str__(self): # теперь в БД во вкладке http://127.0.0.1:8000/admin/news_app/post/ названия постов
        return f'{self.title} | {self.author}'   # f'{self.name.title()}: {self.description[:20]}' в продуктах так было
    class Meta: # меняем в админке названия моделей на удобоваримый
        verbose_name = 'Пост'
        verbose_name_plural = 'Пост-ы'

    def get_absolute_url(self):
        return f'/post/{self.id}' # было так, но зачем так сложно? reverse('news_detail', args=[str(self.id)])

    # Когда объект меняется его надо удалять из кэша, чтобы ключ сбрасывался и больше не находился.
    def save(self, *args, **kwargs): # переопределим метод save для кеширования как только статься будет изменена
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta: # меняем в админке названия моделей на ru
        verbose_name = 'Категория новости'
        verbose_name_plural = 'Категории новостей'

class Comment (models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default="Текст отсутствует")
    time_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()
    def dislike(self):
        self.comment_rating -= 1
        self.save()

    class Meta: # меняем в админке названия моделей на удобоваримый
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self): # теперь в БД во вкладке http://127.0.0.1:8000/admin/news_app/post/ названия коммент
        return self.comment_text



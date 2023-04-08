from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum  # for aggregate суммирование рейтинга методом Sum


class Author(models.Model):
    author_rating = models.IntegerField(default=0)
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)

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
    name_category = models.CharField(max_length=64, unique=True)

class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    N_or_A = [(NEWS, 'Новость'), (ARTICLE, 'Статья')]

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    news_or_article = models.CharField(max_length=2, choices=N_or_A, default=NEWS)
    date_in = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField(default="Текст отсутствует")
    post_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()
    def dislike(self):
         self.post_rating -= 1
         self.save()
    def preview(self):
        return f'{self.text[0:123]}...' # простая версия self.text[0:123]} + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

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

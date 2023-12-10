from rest_framework import serializers  # Dj Rest Framework
from .models import Category, Post


class NewsSerializer(serializers.ModelSerializer):
   class Meta:
       model = Post
       fields = ['id', 'author', 'title', 'text', 'post_category', 'date_in', 'news_or_article', ]


# class ArticlesSerializer(serializers.ModelSerializer): # почему то не идет, либо News либо Articles
#    class Meta:
#        model = Post
#        fields = ['id', 'author', 'title', 'post_category', 'news_or_article', ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Category
       fields = ['id', 'name_category', ]




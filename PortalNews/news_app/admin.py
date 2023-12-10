from django.contrib import admin
from .models import Author, Post, Category, PostCategory, Comment
from modeltranslation.admin import TranslationAdmin # перевод ru-en

# В админке в поле Посты теперь 3 поля. М2М нельзя
class PostAdmin(admin.ModelAdmin): # D-11
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с постами
    list_display = ('title', 'author', 'date_in') # генерируем список нужных полей для более красивого отображения
    list_filter = ('title', 'date_in') # фильтрация по полям
    search_fields = ('title', 'text')        # поиск по полям

#Регистрируем модели для перевода на рус в админке
class Category_Admin(TranslationAdmin):
    model = Category
class Post_Admin(TranslationAdmin):
    model = Post

admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)

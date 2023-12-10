from .models import Post, Category
import django_filters
from django.forms import DateInput

class PostFilter(django_filters.FilterSet): # это фильтр для шаблона search, по каким полям искать
    date = django_filters.DateFilter(field_name='date_in', lookup_expr='lt',
        widget=DateInput(attrs={'type': 'date'}), label='Посты созданные до выбранной даты',)
    title = django_filters.CharFilter(lookup_expr='icontains', label='Поиск по названию поста')
    category = django_filters.ModelChoiceFilter(
        field_name='post_category',    # название поля категории из модели Post
        queryset=Category.objects.all(), # отсюда берем все поля модели Category
        label='Категория',
        empty_label='Выбери категорию',)


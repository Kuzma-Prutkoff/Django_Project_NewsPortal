# from .models import Post, Category
# from django_filters import FilterSet, CharFilter
# import django_filters
#
# class PostFilter(FilterSet):
#     category = CharFilter(field_name='post_category__name', label='Category', lookup_expr='icontains')
#     # category = django_filters.ModelChoiceFilter(
#     #     field_name='post_category',
#     #     queryset=Category.objects.all(),
#     #     label='Category',
#     #     empty_label='Select a category',)
#
#     class Meta:
#         model = Post
#         # В fields мы описываем по каким полям модели будет производиться фильтрация.
#         fields = {'title': ['icontains'],}
#
#     # class Meta:
#     #     model = Post
#     #     fields = ['title', 'post_category', 'date_in',]

from .models import Post
import django_filters
from django.forms import DateInput

class PostFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date_in', lookup_expr='lt',
        widget=DateInput(attrs={'type': 'date'}), label='Посты созданные позже выбранной даты',)

    title = django_filters.CharFilter(lookup_expr='icontains',)

    class Meta:
        model = Post
        fields = ['post_category',]


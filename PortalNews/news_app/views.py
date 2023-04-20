from django.views.generic import ListView, DetailView, CreateView, UpdateView ,DeleteView
from datetime import datetime
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy

class NewsList(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5

    # все эти функции больше не нужны на главной странице и перенесены в PostSearch
    # def get_queryset(self):  # Переопределяем функцию получения списка новостей
    #     queryset = super().get_queryset() # Получаем обычный запрос
    #     # Используем наш класс фильтрации.self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните
    #     #  ранее. Сохраняем нашу фильтрацию в объекте класса,чтобы потом добавить в контекст и использовать в шаблоне.
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return self.filterset.qs # Возвращаем из функции отфильтрованный список товаров
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['time_now'] = datetime.utcnow()
    #     context['next_news'] = "Самая Самая свежая новость"
    #     context['filterset'] = self.filterset  # Добавляем в контекст объект фильтрации.
    #     return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = 'title'
    paginate_by = 5
    def get_queryset(self):  # Переопределяем функцию получения списка новостей
        queryset = super().get_queryset() # Получаем обычный запрос
        # Используем наш класс фильтрации.self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните
        #  ранее. Сохраняем нашу фильтрацию в объекте класса,чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs # Возвращаем из функции отфильтрованный список товаров
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset  # Добавляем в контекст объект фильтрации.
        return context

class NewsCreate(CreateView):
    form_class = PostForm # Указываем нашу разработанную форму
    model = Post # модель товаров
    template_name = 'post_edit.html' # и новый шаблон, в котором используется форма.
    def form_valid(self, form): #В представлении, которое наследует CreateView, переопределяем метод form_valid
        post = form.save(commit=False)
        post.news_or_article = 'NW' # сразу же присвоим полю значение "новость"
        return super().form_valid(form) #запустим механизм сохранения, который вызовет form.save(commit=True).

class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_or_article = 'AR' # сразу же присвоим полю значение "статья"
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

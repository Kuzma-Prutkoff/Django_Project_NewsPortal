from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from datetime import datetime
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

class NewsList(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'news.html'
    context_object_name = 'news' #имя для шаблона
    paginate_by = 5

class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = '-date_in'
    paginate_by = 5

    def get_queryset(self):  # Переопределяем функцию получения списка новостей
        queryset = super().get_queryset() # Получаем обычный запрос
        # Используем наш класс фильтрации.self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните
        #  ранее. Сохраняем нашу фильтрацию в объекте класса,чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs # Возвращаем из функции отфильтрованный список новостей
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset  # Добавляем в контекст объект фильтрации.
        return context

class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    raise_exception = True
    permission_required = ('news_app.add_post',) # есть ли права у юзера делать это
    def form_valid(self, form): #В представлении, которое наследует CreateView, переопределяем метод form_valid
        post = form.save(commit=False)
        post.news_or_article = 'NW' # сразу же присвоим полю значение "новость"
        return super().form_valid(form) #запустим механизм сохранения, который вызовет form.save(commit=True).

class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    raise_exception = True
    permission_required = ('news_app.add_post',) # есть ли права у юзера делать это
    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_or_article = 'AR' # сразу же присвоим полю значение "статья"
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news_app.change_post',) # есть ли права у юзера делать это

class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news_app.delete_post',) # есть ли права у юзера делать это


from django.shortcuts import get_object_or_404
from .models import Category
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render

class CategoryListView(NewsList): # Создаем страницу в которой посты отфильтрованы по категориям. наследуемся от вью NewsList.
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'  # имя по которому мы будем обращаться к данному вью в шаблоне

    def get_queryset(self): # будем получать на 'post/categories/<int:pk>' отфильтрованные по=id категории
        self.post_category = get_object_or_404(Category, id=self.kwargs['pk']) #если категорию удалили, а мы к ней обратимся по id, то ошибка 404 не повесит сервер
        queryset = Post.objects.filter(post_category=self.post_category).order_by('-date_in') #вернем queryset без 404 ошибке и отфильтруем его по дате создания -date_in
        return queryset
    #добавим кнопку подписаться-отписаться
    def get_context_data(self, **kwargs): # добавили 2 переменные is_not_suscriber и category. использ их в шаблоне category_list.html
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.post_category.subscribers.all()
        context['subscriber'] = self.request.user in self.post_category.subscribers.all()
        context['category'] = self.post_category
        return context

@login_required # ПОДПИСАТЬСЯ только зарегистрированные пользователи
@csrf_protect   # автоматически проверяется CSRF-токен в получаемых формах
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message}) # и передадим 2 перем category,message

@login_required # ОТПИСАТЬСЯ только зарегистрированные пользователи
@csrf_protect
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'Вы успешно отписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})

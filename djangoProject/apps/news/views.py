from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, UpdateView, CreateView, DetailView # импоритируем необходимые дженерики

from django.core.paginator import Paginator

from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm


# из списка на главной странице уберём всё лишнее
class Posts(ListView):
    model = Post
    template_name = 'flatpages/post_list.html'
    context_object_name = 'products'
    ordering = ['-rating']
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        # берём значения для нового товара из POST-запроса отправленного на сервер
        form = self.form_class(request.POST) # создаём новую форму, забиваем в неё данные из POST запроса

        if form.is_valid(): # если пользователь ввёл всё правильно и нигде не накосячил то сохраняем новый товар
            form.save()
        return super().get(request, *args, **kwargs) # отправляем пользователя обратно на GET-запрос.


# дженерик для получения деталей о товаре
class PostDetailView(DetailView):
    template_name = 'flatpages/post_detail.html'
    queryset = Post.objects.all()


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(CreateView):
    template_name = 'flatpages/post_create.html'
    form_class = PostForm

class PostUpdateView(UpdateView):
    template_name = 'flatpages/post_create.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'flatpages/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'

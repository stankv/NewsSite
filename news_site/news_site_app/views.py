from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *

# Create your views here.
menu = [{"title":"О сайте", "url_name": "about"},
        {"title":"Добавить статью", "url_name": "add_page"},
        {"title":"Обратная связь", "url_name": "contact"},
        {"title":"Войти", "url_name": "login"},
]

#----------------------------------------------------------------------------------------------------------------------
# представление как функция
# def index(request):
#     posts = Article.objects.all()
#     cats = Category.objects.all()
#     context = {
#         "posts": posts,
#         "cats": cats,
#         "menu": menu,
#         "title": "Главная страница",
#         "cat_selected":0,
#     }
#     return render(request, 'news_site_app/index.html', context=context)


# представление как класс
class IndexView(ListView):
    model = Article
    template_name = 'news_site_app/index.html'    # указываем путь к нашему шаблону, а не article_list.html
    context_object_name = 'posts'    # указываем posts для цикла в index.html, а не object_list

    # для передачи в шаблон контекста объекта списка постов menu
    def get_context_data(self, *, object_list=None, **kwargs):
        cats = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['cats'] = cats
        context['cat_selected'] = 0    # чтобы в меню пункт Все категории был выбранным ("нажатым"
        return context

    # чтобы отображались только те статьи, что отмечены для публикации
    def get_queryset(self):
        return Article.objects.filter(is_published=True)
#----------------------------------------------------------------------------------------------------------------------


def about(request):
    cats = Category.objects.all()
    return render(request, 'news_site_app/about.html', {"menu": menu,
                                                        "cats": cats, "title": "О сайте"})


#----------------------------------------------------------------------------------------------------------------------
# def addpage(request):
#     cats = Category.objects.all()
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # try:
#             #     Article.objects.create(**form.cleaned_data)    # так если форма не связана с моделью
#             #     return  redirect('home')
#             # except:
#             #     form.add_error(None, "Не удалось добавить статью")
#             form.save()  # так если форма связана с моделью, try-except не нужен
#     else:
#         form = AddPostForm()
#     return render(request, 'news_site_app/addpage.html', {"cats": cats, "form": form, "menu": menu, "title": "Добавить статью"})

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'news_site_app/addpage.html'
    success_url = reverse_lazy('home')    # адрес куда будет перенаправлен после успешной отправки формы
                                          # это нужно когда нет функций get_absolute_url()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cats = Category.objects.all()
        context['title'] = 'Добавление статьи'
        context['menu'] = menu
        context['cats'] = cats
        return context
#----------------------------------------------------------------------------------------------------------------------

def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


#----------------------------------------------------------------------------------------------------------------------
# представление как функция
# def show_category(request, cat_slug):
#     cat = get_object_or_404(Category, slug=cat_slug)
#     cats = Category.objects.all()
#     posts = Article.objects.filter(category=cat)
#     if len(posts) == 0:
#         raise Http404
#
#     context = {
#         "posts": posts,
#         "cats": cats,
#         "menu": menu,
#         "title": f"Новости по категории {cat.name}",
#         "cat_selected": cat.id,
#     }
#     return render(request, 'news_site_app/index.html', context=context)

# представление как класс
class ArticleCategory(ListView):
    model = Article
    template_name = 'news_site_app/index.html'
    context_object_name = 'posts'
    allow_empty = False    # генерирует ошибку 404, если выход за пределы массива posts (или нет такого слага)

    def get_queryset(self):
        return Article.objects.filter(category__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        cats = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].category)
        context['menu'] = menu
        context['cats'] = cats
        context['cat_selected'] = context['posts'][0].category_id
        return context
#----------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------
# def show_post(request, post_slug):
#     post = get_object_or_404(Article, slug=post_slug)
#     cats = Category.objects.all()
#     context = {
#         "post": post,
#         "cats": cats,
#         "menu": menu,
#         "title": post.title,
#         "cat_selected": post.category_id,
#     }
#     return render(request, 'news_site_app/post.html', context=context)

class ShowPost(DetailView):
    model = Article
    template_name = 'news_site_app/post.html'
    slug_url_kwarg = 'post_slug'    # указываем наше название вместо slug по умолчанию
    # pk_url_kwarg = 'post_id'    # указываем наше название вместо id по умолчанию
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cats = Category.objects.all()
        context['title'] = context['post']
        context['menu'] = menu
        context['cats'] = cats
        return context
#----------------------------------------------------------------------------------------------------------------------

# обработка несуществующего маршрута (страницы) - возврат страницы 404
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

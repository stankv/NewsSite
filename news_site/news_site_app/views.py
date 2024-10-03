from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404

from .models import *

# Create your views here.
menu = [{"title":"О сайте", "url_name": "about"},
        {"title":"Добавить статью", "url_name": "add_page"},
        {"title":"Обратная связь", "url_name": "contact"},
        {"title":"Войти", "url_name": "login"},
]

def index(request):
    posts = Article.objects.all()
    cats = Category.objects.all()
    context = {
        "posts": posts,
        "cats": cats,
        "menu": menu,
        "title": "Главная страница",
        "cat_selected":0,
    }
    return render(request, 'news_site_app/index.html', context=context)


def about(request):
    return render(request, 'news_site_app/about.html', {"menu": menu, "title": "О сайте"})


def addpage(request):
    return HttpResponse('Добавление статьи')


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


def show_category(request, cat_id):
    posts = Article.objects.filter(category=cat_id)
    cats = Category.objects.all()
    if len(posts) == 0:
        raise Http404

    context = {
        "posts": posts,
        "cats": cats,
        "menu": menu,
        "title": "Отображение по рубрикам",
        "cat_selected": cat_id,
    }
    return render(request, 'news_site_app/index.html', context=context)


def show_post(request, post_id):
    post = get_object_or_404(Article, pk=post_id)
    context = {
        "post": post,
        #"cats": cats,
        "menu": menu,
        "title": post.title,
        "cat_selected": post.category_id,
    }
    return render(request, 'news_site_app/post.html', context=context)


# обработка несуществующего маршрута (страницы) - возврат страницы 404
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

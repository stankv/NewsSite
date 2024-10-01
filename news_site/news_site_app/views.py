from lib2to3.fixes.fix_input import context

from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from .models import *

# Create your views here.
menu = [{"title":"О сайте", "url_name": "about"},
        {"title":"Добавить статью", "url_name": "add_page"},
        {"title":"Обратная связь", "url_name": "contact"},
        {"title":"Войти", "url_name": "login"},
]

def index(request):
    posts = Article.objects.all()
    context = {
        "posts": posts,
        "menu": menu,
        "title": "Главная страница"
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


def show_post(request, post_id):
    return HttpResponse(f'Отображение статьи с id {post_id}')


# обработка несуществующего маршрута (страницы) - возврат страницы 404
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

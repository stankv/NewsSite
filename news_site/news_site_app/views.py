from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *

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
class IndexView(DataMixin, ListView):
    model = Article
    template_name = 'news_site_app/index.html'    # указываем путь к нашему шаблону, а не article_list.html
    context_object_name = 'posts'    # указываем posts для цикла в index.html, а не object_list

    # для передачи в шаблон контекста объекта списка постов menu
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    # чтобы отображались только те статьи, что отмечены для публикации
    def get_queryset(self):
        return Article.objects.filter(is_published=True).select_related('category')    # убрали дублирование sql-запросов
#----------------------------------------------------------------------------------------------------------------------


# def about(request):
#     cats = Category.objects.all()
#     return render(request, 'news_site_app/about.html', {"menu": menu,
#                                                         "cats": cats, "title": "О сайте"})

class AboutView(DataMixin, TemplateView):
    template_name = 'news_site_app/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте')
        return dict(list(context.items()) + list(c_def.items()))


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

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'news_site_app/addpage.html'
    success_url = reverse_lazy('home')    # адрес куда будет перенаправлен после успешной отправки формы
                                          # это нужно когда нет функций get_absolute_url()
    login_url = reverse_lazy('home')
    raise_exception = True                # если True, то будет выброшено исключение Http403 (доступ запрещен)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))
#----------------------------------------------------------------------------------------------------------------------

# def contact(request):
#     return HttpResponse('Обратная связь')


class ContactFormView(DataMixin, FormView):    # FormView не привязан к модели
    form_class = ContactForm
    template_name = 'news_site_app/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


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
class ArticleCategory(DataMixin, ListView):
    model = Article
    template_name = 'news_site_app/index.html'
    context_object_name = 'posts'
    allow_empty = False    # генерирует ошибку 404, если выход за пределы массива posts (или нет такого слага)

    def get_queryset(self):
        return Article.objects.filter(category__slug=self.kwargs['cat_slug'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].category),
        #                               cat_selected=context['posts'][0].category_id)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


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

class ShowPost(DataMixin, DetailView):
    model = Article
    template_name = 'news_site_app/post.html'
    slug_url_kwarg = 'post_slug'    # указываем наше название вместо slug по умолчанию
    # pk_url_kwarg = 'post_id'    # указываем наше название вместо id по умолчанию
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

#----------------------------------------------------------------------------------------------------------------------
# def login(request):
#     return HttpResponse('Авторизация')

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'news_site_app/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    # автоматическое перенаправление на главную стр. при успешной регистрации
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'news_site_app/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')
#----------------------------------------------------------------------------------------------------------------------

# обработка несуществующего маршрута (страницы) - возврат страницы 404
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def logout_user(request):
    logout(request)
    return redirect('login')

#----------------------------------------------------------------------------------------------------------------------
# DRF
#----------------------------------------------------------------------------------------------------------------------

from rest_framework import generics, viewsets
from .serializers import ArticleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms import model_to_dict
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#
#     @action(methods=['get'], detail=False)
#     def categories(self, request):
#         cats = Category.objects.all()
#         return Response({'categories': [c.name for c in cats]})
#
#     @action(methods=['get'], detail=True)
#     def category(self, request, pk=None):
#         cat = Category.objects.get(pk=pk)
#         return Response({'category': cat.name})

class ArticleAPIList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

class ArticleAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class ArticleAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAdminOrReadOnly,)


# class ArticleAPIView(APIView):
#     def get(self, request):    # метод для работы с GET запросами
#         a = Article.objects.all()
#         return Response({'articles': ArticleSerializer(a, many=True).data})    # Response преобразует словарь в JSON-строку
#                                                                           # many - обрабатывать не одну, а несколько записей
#     def post(self, request, *args, **kwargs):    # метод для работы с POST запросами
#         serializer = ArticleSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)    # - проверяет валидность данных
#         serializer.save()
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({"error": "Method Put not allowed"})
#         try:
#             instance = Article.objects.get(pk=pk)
#         except:
#             return Response({"error": "Article not found"})
#         serializer = ArticleSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#         instance = Article.objects.get(pk=pk)
#         instance.delete()
#
#         return Response({"post": "delete post " + str(pk)})

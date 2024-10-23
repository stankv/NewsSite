from django.urls import path, re_path
from .views import *

urlpatterns = [
    # path('', index, name='home'),    # для вьюхи-функции
    path('', IndexView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    # path('categories/', categories),
    path('category/<slug:cat_slug>/', ArticleCategory.as_view(), name='category'),
    #re_path(r'^archive/(?P<year>[0-9]{4})/', archive)
]

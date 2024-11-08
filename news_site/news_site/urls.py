"""
URL configuration for news_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin

from news_site import settings
from news_site_app.views import *
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/articlelist/', ArticleAPIList.as_view()),
    path('api/v1/articlelist/<int:pk>/', ArticleAPIList.as_view()),
    path('captcha/', include('captcha.urls')),
    path('', include('news_site_app.urls')),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = page_not_found

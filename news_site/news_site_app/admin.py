from django.contrib import admin

from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') # отображение столбцов
    list_display_links = ('id', 'name')    # отображение как ссылки
    search_fields = ('name',)    # по каким полям можно делать поиск

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category','time_create', 'photo', 'is_published')  # отображение столбцов
    list_display_links = ("id", "title")  # отображение как ссылки
    search_fields = ('title', 'content')  # по каким полям можно делать поиск

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)


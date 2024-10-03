from django.contrib import admin

from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') # отображение столбцов
    list_display_links = ('id', 'name')    # отображение как ссылки
    search_fields = ('name',)    # по каким полям можно делать поиск
    prepopulated_fields = {'slug': ('name',)}

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category','time_create', 'photo', 'is_published')  # отображение столбцов
    list_display_links = ("id", "title")  # отображение как ссылки
    search_fields = ('title', 'content')  # по каким полям можно делать поиск
    list_editable = ('is_published',)     # задаем возможность редактировать поля прямо в таблице
    list_filter = ('is_published', 'time_create')  # задаем возможность фильтрации
    prepopulated_fields = {'slug': ('title',)} # задаем значение поля slug

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)


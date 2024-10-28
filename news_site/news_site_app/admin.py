from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') # отображение столбцов
    list_display_links = ('id', 'name')    # отображение как ссылки
    search_fields = ('name',)    # по каким полям можно делать поиск
    prepopulated_fields = {'slug': ('name',)}

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category','time_create', 'get_html_photo', 'is_published')  # отображение столбцов
    list_display_links = ("id", "title")  # отображение как ссылки
    search_fields = ('title', 'content')  # по каким полям можно делать поиск
    list_editable = ('is_published',)     # задаем возможность редактировать поля прямо в таблице
    list_filter = ('is_published', 'time_create')  # задаем возможность фильтрации
    prepopulated_fields = {'slug': ('title',)} # задаем значение поля slug
    fields = ('title', 'slug', 'category', 'content', 'photo',     # список и порядок полей, доступных для редактирования
              'get_html_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')    #отображение полей только для чтения
    save_on_top = True    # кнопки сохранить, удалить и т.д. также и вверху

    # вывод фото к постам в админ-панели
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Картинка"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)

admin.site.site_header = 'Админ-панель сайта News Site'
admin.site.site_title = 'Админ-панель сайта News Site'

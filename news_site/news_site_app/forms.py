from django import forms
from .models import *


# Форма для добавления статьи на сайт
class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label='Название статьи')
    slug = forms.SlugField(max_length=255, label='URL')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Текст статьи')
    is_published = forms.BooleanField(label='Опубликовать', required=False, initial=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Выберите категорию',)    # выпадающий список всех категорий


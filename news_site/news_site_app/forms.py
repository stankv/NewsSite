from django import forms
from django.core.exceptions import ValidationError

from .models import *


# Форма для добавления статьи на сайт (если бы форма не была связана с моделью)
# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label='Название статьи')
#     slug = forms.SlugField(max_length=255, label='URL')
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Текст статьи')
#     is_published = forms.BooleanField(label='Опубликовать', required=False, initial=True)
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Выберите категорию',)    # выпадающий список всех категорий

# Если форма связана с моделью
class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):    # конструктор вызывается для изменения значения поля по умолчанию
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Выберите категорию"

    class Meta:
        model = Article        # указываем связь с моделью
        #fields = '__all__'    # отображать все поля
        fields = ['title', 'slug', 'content','photo', 'is_published', 'category']    # отображать только эти поля
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    # Свой валидатор
    def clean_title(self):    # всегда начинается с clean, далее имя проверяемого поля
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return title

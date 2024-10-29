from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):    # сериализатор, работающий с моделью
    class Meta:
        model = Article
        fields = ('title', 'category_id')    # поля, которые будут сериализованы

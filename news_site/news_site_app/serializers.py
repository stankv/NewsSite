from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Article
        fields = ('title', 'slug', 'content', 'category', 'user')
        # fields = '__all__'    # all fields


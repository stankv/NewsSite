from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    slug = serializers.SlugField()
    content = serializers.CharField()
    photo = serializers.ImageField(read_only=True)
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    category_id = serializers.IntegerField()    # category = serializers.CharField()

    def create(self, validated_data):
        return Article.objects.create(**validated_data)    # validated_data - словарь проверенных данных из post-запроса

    def update(self, instance, validated_data):    # instance - ссылается на объект Article
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.content = validated_data.get('content', instance.content)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.time_update = validated_data.get('time_update', instance.time_update)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.save()
        return instance


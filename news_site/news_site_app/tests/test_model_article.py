from django.test import TestCase

from news_site_app.models import Article, Category


# Create your tests here.
class ArticleModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Politika', slug='politika')
        Article.objects.create(title='Statya1', slug='statya1', content='Statya 1', category=Category.objects.get(pk=1))
        cls.obj = Article.objects.get(pk=1)

    def test_title_max_length(self):
        max_len = self.obj._meta.get_field('title').max_length
        self.assertEqual(max_len, 255)

    def test_title_verbose_name(self):
        verbose_name = self.obj._meta.get_field('title').verbose_name
        self.assertEqual(verbose_name, 'Название')

    def test_slug_max_length(self):
        max_len = self.obj._meta.get_field('slug').max_length
        self.assertEqual(max_len, 255)

    def test_slug_verbose_name(self):
        verbose_name = self.obj._meta.get_field('slug').verbose_name
        self.assertEqual(verbose_name, 'URL')

    def test_slug_unique(self):
        unique= self.obj._meta.get_field('slug').unique
        self.assertTrue(unique)

    def test_slug_db_index(self):
        slug_db_index = self.obj._meta.get_field('slug').db_index
        self.assertTrue(slug_db_index)

    def test_content_blank(self):
        self.assertTrue(self.obj._meta.get_field('content').blank)

    def test_content_verbose_name(self):
        verbose_name = self.obj._meta.get_field('content').verbose_name
        self.assertEqual(verbose_name, 'Содержание')

    def test_photo_upload_to(self):
        upload_to = self.obj._meta.get_field('photo').upload_to
        self.assertEqual(upload_to, 'photos/%Y/%m/%d/')

    def test_photo_null(self):
        self.assertTrue(self.obj._meta.get_field('photo').null)

    def test_photo_blank(self):
        self.assertTrue(self.obj._meta.get_field('photo').blank)

    def test_photo_verbose_name(self):
        verbose_name = self.obj._meta.get_field('photo').verbose_name
        self.assertEqual(verbose_name, 'Изображение')

    def test_time_create_auto_now_add(self):
        self.assertTrue(self.obj._meta.get_field('time_create').auto_now_add)

    def test_time_create_verbose_name(self):
        verbose_name = self.obj._meta.get_field('time_create').verbose_name
        self.assertEqual(verbose_name, 'Время создания')

    def test_time_update_auto_now(self):
        self.assertTrue(self.obj._meta.get_field('time_update').auto_now)

    def test_time_update_verbose_name(self):
        verbose_name = self.obj._meta.get_field('time_update').verbose_name
        self.assertEqual(verbose_name, 'Время изменения')

    def test_is_published_default(self):
        self.assertTrue(self.obj._meta.get_field('is_published').default)

    def test_is_published_verbose_name(self):
        verbose_name = self.obj._meta.get_field('is_published').verbose_name
        self.assertEqual(verbose_name, 'Опубликовано')

    def test_category_verbose_name(self):
        verbose_name = self.obj._meta.get_field('category').verbose_name
        self.assertEqual(verbose_name, 'Рубрика')

    def test_get_absolute_url(self):
        url = self.obj.get_absolute_url()
        self.assertEqual(url, '/post/statya1/')

    def test_meta_verbose_name(self):
        verbose_name = self.obj._meta.verbose_name
        self.assertEqual(verbose_name, 'Статьи')

    def test_meta_verbose_name_plural(self):
        verbose_name = self.obj._meta.verbose_name_plural
        self.assertEqual(verbose_name, 'Статьи')

    def test_meta_ordering(self):
        self.assertEqual(self.obj._meta.ordering, ['-time_create', 'title'])

    def test_str(self):
        self.assertEqual(str(self.obj), self.obj.title)


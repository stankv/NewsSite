from django.test import TestCase

from news_site_app.models import Article, Category


# Create your tests here.
class CategoryModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Politika', slug='politika')
        cls.obj = Category.objects.get(pk=1)


    def test_name_max_length(self):
        max_len = self.obj._meta.get_field('name').max_length
        self.assertEqual(max_len, 100)

    def test_slug_max_length(self):
        max_len = self.obj._meta.get_field('slug').max_length
        self.assertEqual(max_len, 255)

    def test_slug_unique(self):
        unique= self.obj._meta.get_field('slug').unique
        self.assertTrue(unique)

    def test_name_verbose_name(self):
        verbose_name = self.obj._meta.get_field('name').verbose_name
        self.assertEqual(verbose_name, 'Рубрика')

    def test_slug_verbose_name(self):
        verbose_name = self.obj._meta.get_field('slug').verbose_name
        self.assertEqual(verbose_name, 'URL')

    def test_all_db_index(self):
        name_db_index = self.obj._meta.get_field('name').db_index
        slug_db_index = self.obj._meta.get_field('slug').db_index
        self.assertTrue(name_db_index)
        self.assertTrue(slug_db_index)

    def test_meta_ordering(self):
        ordering = self.obj._meta.ordering
        self.assertEqual(ordering, ['id'])

    def test_meta_verbose_name(self):
        verbose_name = self.obj._meta.verbose_name
        self.assertEqual(verbose_name, 'Рубрика')

    def test_meta_verbose_name_plural(self):
        verbose_name_plural = self.obj._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Рубрики')

    def test_get_absolute_url(self):
        self.assertEqual(self.obj.get_absolute_url(), '/category/politika/')

    def test_str(self):
        self.assertEqual(str(self.obj), self.obj.name)

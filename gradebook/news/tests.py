from django.test import TestCase, Client
from django.urls import reverse
from .models import News, Teacher


class NewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = Teacher.objects.create(email='testuser', password='testpass')
        self.news1 = News.objects.create(title='News 1', content='Content 1', author=self.teacher)
        self.news2 = News.objects.create(title='News 2', content='Content 2', author=self.teacher)

    def test_news_list_page(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'News 1')
        self.assertContains(response, 'News 2')

    def test_news_pagination(self):
        for _ in range(10):
            News.objects.create(title='News', content='Content', author=self.teacher)
        response = self.client.get(reverse('news_list'))
        self.assertEqual(len(response.context['page_obj']), 5)

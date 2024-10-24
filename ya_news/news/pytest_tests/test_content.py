import pytest
from django.urls import reverse
from news.models import News
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_homepage_news_count(client, news_data):
    """
    Проверяет, что на главной странице не отображается больше
    10 новостей.
    """
    url = reverse('news:home')
    response = client.get(url)
    assert len(response.context['news_list']) <= 10


def test_news_ordering(news_and_comments_data):
    """
    Проверяет, что новости сортируются по дате в порядке
    убывания (новейшие сначала).
    """
    news_list = news_and_comments_data['news_list']
    sorted_news = News.objects.order_by('-date')
    assert list(sorted_news) == news_list[::-1]


@pytest.mark.django_db
def test_comment_ordering(news_and_comments_data):
    """
    Проверяет, что комментарии к новости сортируются по дате
    создания в порядке возрастания (старые комментарии первыми).
    """
    comments = news_and_comments_data['comments']
    news = news_and_comments_data['news_list'][0]
    sorted_comments = news.comment_set.order_by('created')
    assert list(sorted_comments) == comments


@pytest.mark.django_db
def test_anonymous_user_cannot_access_comment_form(client):
    """
    Проверяет, что анонимные пользователи не могут видеть
    форму для комментариев на странице новости.
    """
    news = News.objects.create(title='Test News', date='2024-10-23')
    url = reverse('news:detail', args=[news.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert 'comment_form' not in response.content.decode()


@pytest.mark.django_db
def test_authenticated_user_can_access_comment_form(client):
    """
    Проверяет, что авторизованные пользователи могут видеть
    форму для комментариев на странице новости.
    """
    news = News.objects.create(title='Test News', date='2024-10-23')
    client.login(username='testuser', password='password')
    url = reverse('news:detail', args=[news.pk])
    response = client.get(url)
    assert response.status_code == 200

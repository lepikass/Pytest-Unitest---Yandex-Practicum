import pytest
from django.contrib.auth.models import User
from news.models import News, Comment
from datetime import datetime, timedelta


@pytest.fixture
def user(db):
    """Создаём тестового пользователя."""
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def author_user(db):
    """Создаём автора комментария."""
    return User.objects.create_user(username='author', password='password')


@pytest.fixture
def auth_client(client, user):
    """Клиент с авторизацией обычного пользователя."""
    client.login(username='testuser', password='password')
    return client


@pytest.fixture
def author_client(client, author_user):
    """Клиент с авторизацией автора комментария."""
    client.login(username='author', password='password')
    return client


@pytest.fixture
def news(db):
    """Создаём тестовую новость."""
    return News.objects.create(title='Test News', text='Some text')


@pytest.fixture
def comment(db, author_user, news):
    """Создаём комментарий от авторизованного пользователя."""
    return Comment.objects.create(
        news=news, author=author_user, text='Test comment'
    )


@pytest.fixture
def news_data(db):
    """
    Создаёт 15 записей новостей для использования в тестах.
    """
    for i in range(15):
        News.objects.create(title=f'News {i}', text='Some text')


@pytest.fixture
def news_and_comments_data(db):
    """
    Создаёт 3 новости с различными датами и 3 комментария для каждой новости.
    """
    news1 = News.objects.create(
        title='News 1', date=datetime.today() - timedelta(days=2)
    )
    news2 = News.objects.create(
        title='News 2', date=datetime.today() - timedelta(days=1)
    )
    news3 = News.objects.create(
        title='News 3', date=datetime.today()
    )
    author = User.objects.create_user(username='testuser', password='password')
    comment1 = Comment.objects.create(
        news=news1, author=author, text='Comment 1',
        created=datetime.now() - timedelta(days=2)
    )
    comment2 = Comment.objects.create(
        news=news1, author=author, text='Comment 2',
        created=datetime.now() - timedelta(days=1)
    )
    comment3 = Comment.objects.create(
        news=news1, author=author, text='Comment 3',
        created=datetime.now()
    )
    return {
        'news_list': [news1, news2, news3],
        'comments': [comment1, comment2, comment3]
    }

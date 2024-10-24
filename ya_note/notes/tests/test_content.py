from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note
from http import HTTPStatus

User = get_user_model()


class NotesTests(TestCase):
    """
    Тесты для работы с заметками, включая создание,
    редактирование и отображение списка заметок.
    """

    @classmethod
    def setUpTestData(cls):
        """Создаёт тестовых пользователей и заметки для тестов."""
        cls.user1 = User.objects.create_user(
            username='user1',
            password='pass1'
        )
        cls.user2 = User.objects.create_user(
            username='user2',
            password='pass2'
        )
        cls.note1 = Note.objects.create(
            title='Note 1',
            text='Text 1',
            author=cls.user1
        )
        cls.note2 = Note.objects.create(
            title='Note 2',
            text='Text 2',
            author=cls.user2
        )

    def setUp(self):
        """Логин пользователя для тестов."""
        self.client.login(username='user1', password='pass1')

    def test_update_note_form_in_context(self):
        """
        Проверяет, что на странице редактирования заметки передаётся форма
        для авторизованного пользователя.
        """
        response = self.client.get(
            reverse('notes:edit', args=[self.note1.slug])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('form', response.context)
        self.assertContains(response, '<form')

    def test_edit_note_access_by_other_user(self):
        """
        Проверяет, что другой пользователь не может
        редактировать чужую заметку.
        """
        # Логин другого пользователя для проверки доступа к чужой заметке
        self.client.logout()
        self.client.login(username='user2', password='pass2')
        response = self.client.get(
            reverse('notes:edit', args=[self.note1.slug])
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

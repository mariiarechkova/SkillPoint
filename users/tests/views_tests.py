from http.client import responses

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User, Profile
from organisations.models import Organisation
from voting.models import VoteEvent


class UserListTestCase(APITestCase):
    def setUp(self):
        # Создаем организацию
        self.organisation = Organisation.objects.create(name="Test Organisation")

        # Создаем двух пользователей
        self.user1 = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            organisation=self.organisation,
            password="password123",
            is_staff=True
        )
        self.user2 = User.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            organisation=self.organisation,
            password="password123",
            is_staff=False
        )

        self.other_user = User.objects.create(
            first_name="Alice",
            last_name="Brown",
            email="alicebrown@example.com",
            organisation=Organisation.objects.create(name="Other Organisation"),
            password="password123",
            is_staff=False
        )

        # Авторизуемся как администратор
        self.client.force_authenticate(user=self.user1)

        self.profile = Profile.objects.create(user=self.user1, job_title = 'simple_job_title')


    def test_get_users_list(self):
        self.url = reverse('users-list')
        # Проверка, что доступ к списку пользователей возможен
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка, что возвращаемый список содержит правильное количество пользователей
        self.assertEqual(len(response.data), 2)

        # Проверка, что данные содержат информацию о пользователях
        self.assertEqual(response.data[0]['first_name'], 'John')
        self.assertEqual(response.data[1]['first_name'], 'Jane')

    def test_user_list_not_authenticated(self):
        self.url = reverse('users-list')
        # Проверка, что доступ к списку пользователей не возможен для неавторизованного пользователя
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_list_filter_by_first_name(self):
        self.url = reverse('users-list')
        # Проверка фильтрации пользователей по имени
        response = self.client.get(self.url, {'search': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ожидаем, что будет найден только один пользователь
        self.assertEqual(response.data[0]['first_name'], 'John')

    def test_user_list_filter_by_last_name(self):
        self.url = reverse('users-list')
        # Проверка фильтрации пользователей по фамилии
        response = self.client.get(self.url, {'search': 'Smith'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ожидаем, что будет найден только один пользователь
        self.assertEqual(response.data[0]['last_name'], 'Smith')

    def test_user_detail_success(self):
        # Тестируем успешный запрос с правильным ID пользователя
        self.url = reverse('user-detail', args=[self.user1.id])
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'john@example.com')
        self.assertIn('job_title', response.data)
        self.assertEqual(response.data['job_title'], 'simple_job_title')

    def test_get_user_not_found(self):
        # Отправляем запрос на несуществующего пользователя
        invalid_url = reverse('user-detail', args=[9999])  # Используем несуществующий ID
        response = self.client.get(invalid_url)

        # Проверяем, что возвращается ошибка 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'User not found')

    def test_get_available_users(self):
        self.url = reverse('available-to-vote')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_ids = [user['id'] for user in response.data]
        self.assertIn(self.user2.id, user_ids)
        self.assertNotIn(self.user1.id, user_ids)  # Текущий пользователь не должен быть в списке
        self.assertNotIn(self.other_user.id, user_ids) # Пользователь из другой организации не должен быть в списке


class RegistrationViewTestCase(APITestCase):

    def setUp(self):
        # Создание тестовой организации и события голосования
        self.organisation = Organisation.objects.create(name="Test Organisation")
        self.vote_event = VoteEvent.objects.create(
            frequency='month',
            start_day=1,
            end_day=15,
            organisation=self.organisation
        )

    def test_registration_with_valid_data(self):
        url = reverse('registration')
        data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice.smith@example.com',
            'password': 'securepassword123',
        }

        response = self.client.post(f"{url}?vote_event_id={self.vote_event.id}", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['first_name'], 'Alice')
        self.assertEqual(response.data['last_name'], 'Smith')
        self.assertEqual(response.data['email'], 'alice.smith@example.com')

    def test_registration_with_missing_vote_event(self):
        url = reverse('registration')
        data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice.smith@example.com',
            'password': 'securepassword123'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверяем правильный формат ошибки
        self.assertEqual(response.data['error'], "vote_event_id is required as a query parameter")



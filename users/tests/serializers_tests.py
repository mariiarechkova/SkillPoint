from django.test import TestCase
from users.models import User
from organisations.models import Organisation
from users.serializers import UserSerializer

class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(name="Test Organisation")
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            organisation=self.organisation,
            is_staff=True
        )
    def test_user_serialization(self):
        """ Проверяем, что сериализатор корректно преобразует объект пользователя в JSON """
        serializer = UserSerializer(instance=self.user)
        expected_data = {
            'id': self.user.id,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'department': None,
            'is_staff': True
        }
        self.assertEqual(serializer.data, expected_data)

    def test_user_validation(self):
        """ Проверяем, что сериализатор отлавливает отсутствие пароля """
        invalid_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.com',
            'organisation': self.organisation.id
            # Нет пароля!
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())  # Данные должны быть невалидными
        self.assertIn('password', serializer.errors)  # Ошибка должна быть связана с паролем

    def test_user_creation(self):
        """ Проверяем, что пользователь создается через сериализатор и пароль хэшируется """
        valid_data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'organisation': self.organisation.id,
            'password': 'securepassword123'
        }
        serializer = UserSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertIsInstance(user, User)  # Проверяем, что объект создан
        self.assertNotEqual(user.password, 'securepassword123')  # Пароль должен быть хэширован
        self.assertTrue(user.check_password('securepassword123'))  # Проверяем, что пароль хэширован правильно
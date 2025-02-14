from django.test import TestCase
from users.models import User, Role
from organisations.models import Organisation
from users.serializers import UserSerializer, RoleSerializer

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

class RoleSerializerTestCase(TestCase):
    def test_serialization(self):
        """check that the serializer correctly converts the Role object to JSON."""
        role = Role.objects.create(title="Manager", weight_vote=5.0)
        serializer = RoleSerializer(instance=role)
        expected_data = {
            "id": role.id,
            "title": "Manager",
            "weight_vote": 5.0,
        }
        self.assertEqual(serializer.data, expected_data)
    def test_valid_weight_vote(self):
        valid_data = {
            'title': "manager",
            'weight_vote': 7.5
        }

        serializer = RoleSerializer(data = valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_weight_vote_high(self):
        invalid_data = {
            'title': "manager",
            'weight_vote': 15.0
        }

        serializer = RoleSerializer(data = invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("weight_vote", serializer.errors)
        self.assertEqual(serializer.errors["weight_vote"][0], 'The score should be from 1.0 to 10.0')

    def test_invalid_weight_vote_low(self):
        invalid_data = {
            'title': "manager",
            'weight_vote': 0.5
        }

        serializer = RoleSerializer(data = invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("weight_vote", serializer.errors)
        self.assertEqual(serializer.errors["weight_vote"][0], 'The score should be from 1.0 to 10.0')

    def test_serializer_created_role(self):
        """We check that the serializer validates and creates the object correctly."""
        valid_data = {
            "title": "Manager",
            "weight_vote": 7.0,
        }
        serializer = RoleSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        role = serializer.save()
        self.assertEqual(role.title, "Manager")
        self.assertEqual(role.weight_vote, 7.0)
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Message

Usuario = get_user_model()

class UsuarioTest(TestCase):

    def setUp(self):
        self.user = Usuario.objects.create_user(
            username="majo",
            password="123456"
        )

    def test_usuario_creado(self):
        self.assertEqual(self.user.username, "majo")
        self.assertTrue(self.user.check_password("123456"))

class MessageTest(TestCase):

    def setUp(self):
        self.user = Usuario.objects.create_user(
            username="test",
            password="123456"
        )

    def test_crear_mensaje(self):
        msg = Message.objects.create(
            user=self.user,
            content="Hola",
            sender_type="user"
        )

        self.assertEqual(msg.content, "Hola")
        self.assertEqual(msg.sender_type, "user")
        self.assertEqual(msg.user.username, "test")

    def test_orden_mensajes(self):
        Message.objects.create(user=self.user, content="1", sender_type="user")
        Message.objects.create(user=self.user, content="2", sender_type="user")

        mensajes = Message.objects.all()

        self.assertEqual(mensajes[0].content, "1")


class RegistroTest(TestCase):

    def setUp(self):
        self.user = Usuario.objects.create_user(
            username="majo",
            password="123456"
        )

    def test_registro_usuario_duplicado_no_500(self):
        response = self.client.post(reverse('register'), {
            'username': 'majo',
            'email': 'majo2@example.com',
            'password1': 'abc123def',
            'password2': 'abc123def'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este nombre de usuario ya está registrado')

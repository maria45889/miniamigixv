from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Message, Estudio, Trabajo, Entretenimiento, Blog, Noticia, Cancion

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
        response = self.client.post(reverse('chat:register'), {
            'username': 'majo',
            'email': 'majo2@example.com',
            'password1': 'abc123def',
            'password2': 'abc123def'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este nombre de usuario ya está registrado')

class NuevosModelosTest(TestCase):
    """
    Pruebas para verificar la correcta creación de los nuevos modelos
    agregados recientemente (Estudios, Trabajos, Entretenimiento, etc.)
    """

    def setUp(self):
        self.user = Usuario.objects.create_user(
            username="tester_modelos",
            password="password123"
        )

    def test_crear_estudio(self):
        estudio = Estudio.objects.create(usuario=self.user, titulo="Examen Django")
        self.assertEqual(estudio.titulo, "Examen Django")
        self.assertFalse(estudio.completado)

    def test_crear_trabajo(self):
        trabajo = Trabajo.objects.create(usuario=self.user, titulo="Proyecto Final")
        self.assertEqual(trabajo.titulo, "Proyecto Final")

    def test_crear_entretenimiento(self):
        ent = Entretenimiento.objects.create(usuario=self.user, titulo="Juego Nuevo", tipo="juego")
        self.assertEqual(ent.tipo, "juego")
        self.assertEqual(ent.titulo, "Juego Nuevo")

    def test_crear_blog(self):
        blog = Blog.objects.create(usuario=self.user, titulo="Mi Post", contenido="Hola Mundo")
        self.assertEqual(blog.titulo, "Mi Post")
        self.assertTrue(blog.publicado)

    def test_crear_noticia(self):
        noticia = Noticia.objects.create(usuario=self.user, titulo="Noticia 1", url="http://example.com")
        self.assertEqual(noticia.titulo, "Noticia 1")
        self.assertFalse(noticia.leida)

    def test_crear_cancion(self):
        cancion = Cancion.objects.create(
            usuario=self.user, 
            titulo="Canción Test", 
            youtube_url="http://youtube.com/watch?v=test"
        )
        self.assertEqual(cancion.titulo, "Canción Test")
        self.assertEqual(cancion.orden, 0)

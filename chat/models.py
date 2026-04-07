from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

class Usuario(AbstractUser):
    bio = models.TextField(blank=True, null=True)

    foto = models.ImageField(
        upload_to='perfiles/',
        default='perfiles/default.png',
        blank=True
    )

    # Nombre personalizado del bot (para cada usuario)
    bot_nombre = models.CharField(max_length=100, default='MiniAmigixV')

    # Racha de días usando la app
    racha_dias      = models.PositiveIntegerField(default=0)
    ultima_visita   = models.DateField(null=True, blank=True)

    # Preferencias visuales (guardadas en BD como respaldo)
    fondo_tipo      = models.CharField(max_length=20, default='gradient')   # gradient | image | pattern
    fondo_valor     = models.CharField(max_length=200, default='')          # color hex, url, nombre patrón
    fuente_chat     = models.CharField(max_length=50, default='DM Sans')    # nombre de la fuente
    musica_activa   = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='usuarios',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarios_permisos',
        blank=True
    )

    def __str__(self):
        return self.username

    def actualizar_racha(self):
        """Llama esto en cada login/visita al index."""
        hoy = timezone.localtime(timezone.now()).date()
        if self.ultima_visita is None:
            self.racha_dias    = 1
            self.ultima_visita = hoy
        else:
            diff = (hoy - self.ultima_visita).days
            if diff == 1:
                self.racha_dias += 1
                self.ultima_visita = hoy
            elif diff > 1:
                self.racha_dias    = 1
                self.ultima_visita = hoy
            # diff == 0: mismo día, no cambia nada
        self.save(update_fields=['racha_dias', 'ultima_visita'])


class Message(models.Model):

    SENDER_CHOICES = [
        ('user',               'Usuario'),
        ('bot',                'Bot'),
        ('event_notification', 'Notificación de evento'),
    ]

    user = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='mensajes'
    )

    sender_type = models.CharField(
        max_length=20,
        choices=SENDER_CHOICES,
        default='user'
    )

    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    read       = models.BooleanField(default=False)

    def __str__(self):
        sender = "MiniAmigixV 💖" if self.sender_type == "bot" else self.user.username
        return f"{sender}: {self.content[:30]}"

    class Meta:
        ordering       = ['created_at']
        verbose_name   = "Mensaje"
        verbose_name_plural = "Mensajes"

class ScheduledMessage(models.Model):

    TIPO_CHOICES = [
        ('checkin',      'Check-in'),
        ('motivacional', 'Motivacional'),
        ('historial',    'Historial'),
        ('saludo',       'Saludo'),
    ]

    user = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='mensajes_programados'
    )

    content          = models.TextField()
    tipo             = models.CharField(max_length=20, choices=TIPO_CHOICES)
    programado_para  = models.DateTimeField(db_index=True)
    entregado        = models.BooleanField(default=False)
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.tipo}] {self.user.username}: {self.content[:30]}"

    class Meta:
        ordering       = ['-programado_para']
        verbose_name   = "Mensaje programado"
        verbose_name_plural = "Mensajes programados"

CATEGORIA_CHOICES = [
    ('general',    '📌 General'),
    ('trabajo',    '💼 Trabajo'),
    ('salud',      '💊 Salud'),
    ('social',     '🎉 Social'),
    ('cumple',     '🎂 Cumpleaños'),
    ('viaje',      '✈️ Viaje'),
    ('otro',       '🔖 Otro'),
]

class Evento(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='eventos'
    )

    titulo      = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha       = models.DateTimeField(db_index=True)
    recordatorio = models.BooleanField(default=True)

    # Color personalizado del evento en el calendario
    color       = models.CharField(max_length=20, default='#e91e63')

    # Categoría
    categoria   = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='general'
    )

    creado_en   = models.DateTimeField(auto_now_add=True)

    # Flags para recordatorios automáticos por bot
    recordatorio_5_dias = models.BooleanField(default=False)
    recordatorio_1_dia  = models.BooleanField(default=False)
    recordatorio_hoy    = models.BooleanField(default=False)

    # Campos legacy (mantenidos por compatibilidad)
    veces_recordado     = models.PositiveIntegerField(default=0)
    veces_recordado_dia = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.titulo} ({self.fecha.strftime('%d/%m/%Y %H:%M')})"

    class Meta:
        ordering       = ['fecha']
        verbose_name   = "Evento"
        verbose_name_plural = "Eventos"
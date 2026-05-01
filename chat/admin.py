from django.contrib import admin
from .models import (
    Usuario, Message, ScheduledMessage, Evento, Task,
    Estudio, Trabajo, Entretenimiento, Blog, Noticia, Cancion
)


# ==============================
# 👤 USUARIO
# ==============================
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)


# ==============================
# 💬 MENSAJES
# ==============================
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'sender_type', 'short_content', 'created_at', 'read')
    list_filter = ('sender_type', 'created_at', 'read')
    search_fields = ('user__username', 'content')
    ordering = ('-created_at',)

    def short_content(self, obj):
        return obj.content[:50] if obj.content else ""
    
    short_content.short_description = "Mensaje"


# ==============================
# ⏰ MENSAJES PROGRAMADOS
# ==============================
@admin.register(ScheduledMessage)
class ScheduledMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo', 'short_content', 'programado_para', 'entregado')
    list_filter = ('tipo', 'entregado')
    search_fields = ('user__username', 'content')
    ordering = ('-programado_para',)

    def short_content(self, obj):
        return obj.content[:50] if obj.content else ""
    
    short_content.short_description = "Mensaje"


# ==============================
# 📅 EVENTOS
# ==============================
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'fecha', 'categoria', 'recordatorio')
    list_filter = ('categoria', 'recordatorio', 'fecha')
    search_fields = ('titulo', 'usuario__username')
    ordering = ('fecha',)


# ==============================
# ✅ TAREAS (TO-DO)
# ==============================
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'completada', 'creada_en')
    list_filter = ('completada', 'creada_en')
    search_fields = ('titulo', 'usuario__username')
    ordering = ('completada', '-creada_en')


# ==============================
# 💖 PERSONALIZACIÓN ADMIN
# ==============================
admin.site.site_header = "MiniAmigixV 💖 Admin"
admin.site.site_title = "MiniAmigixV"
admin.site.index_title = "Panel de administración"


# ==============================
# 📚 ESTUDIOS
# ==============================
@admin.register(Estudio)
class EstudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'fecha_entrega', 'completado')
    list_filter = ('completado', 'fecha_entrega')

# ==============================
# 💼 TRABAJOS
# ==============================
@admin.register(Trabajo)
class TrabajoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'fecha_limite', 'completado')
    list_filter = ('completado', 'fecha_limite')

# ==============================
# 🍿 ENTRETENIMIENTO
# ==============================
@admin.register(Entretenimiento)
class EntretenimientoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'tipo', 'completado')
    list_filter = ('tipo', 'completado')

# ==============================
# 📝 BLOG
# ==============================
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'publicado', 'creado_en')
    list_filter = ('publicado', 'creado_en')

# ==============================
# 📰 NOTICIAS
# ==============================
@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'fuente', 'leida')
    list_filter = ('leida', 'fuente')

# ==============================
# 🎵 MÚSICA (CANCIONES)
# ==============================
@admin.register(Cancion)
class CancionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'duracion', 'orden')
    list_filter = ('usuario',)
    ordering = ('orden',)

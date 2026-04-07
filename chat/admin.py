from django.contrib import admin
from .models import Usuario, Message, ScheduledMessage


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
# 💖 PERSONALIZACIÓN ADMIN
# ==============================
admin.site.site_header = "MiniAmigixV 💖 Admin"
admin.site.site_title = "MiniAmigixV"
admin.site.index_title = "Panel de administración"
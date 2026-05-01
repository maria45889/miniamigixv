from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),

    # Autenticación
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('registro/', views.register_view, name='register'),

    # Chat
    path('send_message/', views.send_message, name='send_message'),
    path('conversaciones/listar/', views.listar_conversaciones, name='listar_conversaciones'),
    path('conversaciones/crear/', views.crear_conversacion, name='crear_conversacion'),
    path('conversaciones/eliminar/<int:conversation_id>/', views.eliminar_conversacion, name='eliminar_conversacion'),
    path('conversaciones/<int:conversation_id>/historial/', views.obtener_historial_chat, name='obtener_historial_chat'),

    # Eventos
    path('eventos/crear/',                    views.crear_evento,          name='create_event'),
    path('eventos/editar/<int:evento_id>/',   views.editar_evento,         name='edit_event'),
    path('eventos/eliminar/<int:evento_id>/', views.eliminar_evento,       name='delete_event'),
    path('eventos/verificar/',                views.verificar_eventos_ajax, name='verificar_eventos_ajax'),
    path('eventos/listar/',                   views.listar_eventos,         name='listar_eventos'),

    # Música
    path('musica/listar/',                    views.listar_canciones,       name='listar_canciones'),
    path('musica/agregar/',                   views.agregar_cancion,        name='agregar_cancion'),
    path('musica/editar/<int:cancion_id>/',   views.editar_cancion,         name='editar_cancion'),
    path('musica/eliminar/<int:cancion_id>/', views.eliminar_cancion,       name='eliminar_cancion'),

    # Blog
    path('blog/listar/',                      views.listar_blogs,           name='listar_blogs'),
    path('blog/crear/',                       views.crear_blog,             name='crear_blog'),

    # Estudios
    path('estudios/listar/',                  views.listar_estudios,        name='listar_estudios'),
    path('estudios/crear/',                   views.crear_estudio,          name='crear_estudio'),

    # Trabajos
    path('trabajos/listar/',                  views.listar_trabajos,        name='listar_trabajos'),
    path('trabajos/crear/',                   views.crear_trabajo,          name='crear_trabajo'),

    # Entretenimiento
    path('entretenimiento/listar/',           views.listar_entretenimiento, name='listar_entretenimiento'),
    path('entretenimiento/crear/',            views.crear_entretenimiento,  name='crear_entretenimiento'),
    path('entretenimiento/toggle/<int:item_id>/', views.toggle_entretenimiento, name='toggle_entretenimiento'),

    # Noticias
    path('noticias/listar/',                  views.listar_noticias,        name='listar_noticias'),
    path('noticias/crear/',                   views.crear_noticia,          name='crear_noticia'),

    # Clima
    path('clima/obtener/',                    views.obtener_clima,          name='obtener_clima'),
    path('clima/actualizar_ciudad/',          views.actualizar_ciudad,      name='actualizar_ciudad'),
]
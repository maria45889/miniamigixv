from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Autenticación
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('registro/', views.register_view, name='register'),

    # Chat
    path('send_message/', views.send_message, name='send_message'),

    # Eventos
    path('eventos/crear/',                    views.crear_evento,          name='create_event'),
    path('eventos/editar/<int:evento_id>/',   views.editar_evento,         name='edit_event'),
    path('eventos/eliminar/<int:evento_id>/', views.eliminar_evento,       name='delete_event'),
    path('eventos/verificar/',                views.verificar_eventos_ajax, name='verificar_eventos_ajax'),
    path('eventos/listar/',                   views.listar_eventos,         name='listar_eventos'),
]
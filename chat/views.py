from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.db import IntegrityError
from django.conf import settings

from .models import Message, ScheduledMessage, Evento
from .forms import RegistroForm

import random
import os
import json

Usuario = get_user_model()

memoria = {}

def inicializar_memoria(user):
    if user.username not in memoria:
        ultimos = Message.objects.filter(user=user).order_by('-created_at')[:10]
        memoria[user.username] = {
            "historial": [m.content.lower() for m in reversed(ultimos)],
        }

def agregar_a_memoria(user, msg):
    if user.username not in memoria:
        inicializar_memoria(user)
    memoria[user.username]["historial"].append(msg.lower())
    memoria[user.username]["historial"] = memoria[user.username]["historial"][-50:]

def generar_respuesta(msg, user):
    msg_lower = msg.lower().strip()
    inicializar_memoria(user)
    agregar_a_memoria(user, msg_lower)

    nombre = user.first_name or user.username

    if "hola" in msg_lower:
        return f"Hola {nombre} 💖 ¿Cómo estás?"
    if "gracias" in msg_lower:
        return f"Siempre para ti {nombre} 💕"
    if "triste" in msg_lower or "mal" in msg_lower:
        return f"Ay {nombre} 🥺 cuéntame qué pasó, estoy contigo 💖"
    if "feliz" in msg_lower or "bien" in msg_lower:
        return f"Qué lindo {nombre} 😊 me alegra mucho 💖"

    return random.choice([
        f"Cuéntame más {nombre} 💕",
        f"Estoy aquí para ti {nombre} 💖",
        f"Te escucho {nombre} 😊",
    ])

def programar_mensajes(user):
    ahora = timezone.localtime(timezone.now())
    hoy = ahora.date()
    if not ScheduledMessage.objects.filter(user=user, created_at__date=hoy).exists():
        ScheduledMessage.objects.create(
            user=user,
            content="Hoy es un buen día 💖",
            tipo="motivacional",
            programado_para=ahora
        )

def entregar_mensajes_programados(user):
    ahora = timezone.localtime(timezone.now())
    pendientes = ScheduledMessage.objects.filter(
        user=user, programado_para__lte=ahora, entregado=False
    )
    for msg in pendientes:
        Message.objects.create(user=user, content=msg.content, sender_type="bot")
        msg.entregado = True
        msg.save()

def verificar_eventos(user):
    ahora = timezone.localtime(timezone.now())
    hoy   = ahora.date()
    # Solo eventos futuros con recordatorio activado
    eventos = Evento.objects.filter(usuario=user, recordatorio=True, fecha__gte=ahora)

    for evento in eventos:
        if not evento.fecha:
            continue

        fecha_evento    = timezone.localtime(evento.fecha).date()
        dias_restantes  = (fecha_evento - hoy).days
        hora_formato    = timezone.localtime(evento.fecha).strftime('%H:%M')
        fecha_formato   = timezone.localtime(evento.fecha).strftime('%d/%m/%Y')

        # 5 días antes
        if dias_restantes == 5 and not evento.recordatorio_5_dias:
            Message.objects.create(
                user=user,
                content=(
                    f"📅 ¡Faltan 5 días para '{evento.titulo}'! "
                    f"Será el {fecha_formato} a las {hora_formato} 💖"
                ),
                sender_type="bot"
            )
            evento.recordatorio_5_dias = True
            evento.save()

        # 1 día antes
        elif dias_restantes == 1 and not evento.recordatorio_1_dia:
            Message.objects.create(
                user=user,
                content=(
                    f"⏰ ¡Mañana es '{evento.titulo}'! "
                    f"A las {hora_formato} 💕 ¡No lo olvides!"
                ),
                sender_type="bot"
            )
            evento.recordatorio_1_dia = True
            evento.save()

        # El mismo día
        elif dias_restantes == 0 and not evento.recordatorio_hoy:
            Message.objects.create(
                user=user,
                content=(
                    f"🎉 ¡Hoy es '{evento.titulo}'! "
                    f"A las {hora_formato} 💖 ¡Ya casi!"
                ),
                sender_type="bot"
            )
            evento.recordatorio_hoy = True
            evento.save()

@login_required
def index(request):
    programar_mensajes(request.user)
    entregar_mensajes_programados(request.user)
    verificar_eventos(request.user)

    mensajes = Message.objects.filter(user=request.user)
    eventos  = Evento.objects.filter(usuario=request.user)

    return render(request, "chat/index.html", {"mensajes": mensajes, "eventos": eventos})

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect("index")
        return render(request, "chat/login.html", {"error": "Credenciales incorrectas"})
    return render(request, "chat/login.html")

def register_view(request):
    form = RegistroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            user = form.save()
        except IntegrityError:
            form.add_error('username', 'Usuario ya existe')
        else:
            login(request, user)
            return redirect("index")
    return render(request, "chat/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def send_message(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido"}, status=405)

    if request.content_type == "application/json":
        data = json.loads(request.body)
        msg  = data.get("content", "").strip()
    else:
        msg = request.POST.get("message", "").strip()

    if not msg:
        return JsonResponse({"reply": "Escribe algo 💖"})

    Message.objects.create(user=request.user, content=msg, sender_type="user")
    reply = generar_respuesta(msg, request.user)
    Message.objects.create(user=request.user, content=reply, sender_type="bot")

    return JsonResponse({"reply": reply})

@login_required
def crear_evento(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "error": "Método no permitido"}, status=405)

    try:
        if request.content_type == "application/json":
            data = json.loads(request.body)
        else:
            data = request.POST

        titulo       = data.get("titulo", "").strip()
        descripcion  = data.get("descripcion", "")
        fecha_str    = data.get("fecha", "")
        recordatorio = data.get("recordatorio") in [True, "true", "on", "True"]
        color        = data.get("color", "#e91e63")
        categoria    = data.get("categoria", "general")

        fecha = parse_datetime(fecha_str)
        if not fecha:
            return JsonResponse({"status": "error", "error": "Fecha inválida"})
        if fecha.tzinfo is None:
            fecha = timezone.make_aware(fecha)

        evento = Evento.objects.create(
            usuario=request.user,
            titulo=titulo,
            descripcion=descripcion,
            fecha=fecha,
            recordatorio=recordatorio,
            color=color,
            categoria=categoria,
        )
        Message.objects.create(
            user=request.user,
            content=f"📅 Evento creado: {evento.titulo}",
            sender_type="event_notification"
        )
        return JsonResponse({"status": "ok", "id": evento.id})

    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)})

@login_required
def editar_evento(request, evento_id):
    if request.method != "POST":
        return JsonResponse({"status": "error", "error": "Método no permitido"}, status=405)

    evento = get_object_or_404(Evento, id=evento_id, usuario=request.user)

    try:
        if request.content_type == "application/json":
            data = json.loads(request.body)
        else:
            data = request.POST

        titulo       = data.get("titulo", "").strip()
        descripcion  = data.get("descripcion", "")
        fecha_str    = data.get("fecha", "")
        recordatorio = data.get("recordatorio") in [True, "true", "on", "True"]
        color        = data.get("color", evento.color)
        categoria    = data.get("categoria", evento.categoria)

        fecha = parse_datetime(fecha_str)
        if not fecha:
            return JsonResponse({"status": "error", "error": "Fecha inválida"})
        if fecha.tzinfo is None:
            fecha = timezone.make_aware(fecha)

        evento.titulo            = titulo
        evento.descripcion       = descripcion
        evento.fecha             = fecha
        evento.recordatorio      = recordatorio
        evento.color             = color
        evento.categoria         = categoria
        # Resetear recordatorios al cambiar fecha
        evento.recordatorio_5_dias = False
        evento.recordatorio_1_dia  = False
        evento.recordatorio_hoy    = False
        evento.save()

        Message.objects.create(
            user=request.user,
            content=f"✏️ Evento actualizado: {evento.titulo}",
            sender_type="event_notification"
        )
        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)})

@login_required
def eliminar_evento(request, evento_id):
    if request.method != "POST":
        return JsonResponse({"status": "error", "error": "Método no permitido"}, status=405)

    evento = get_object_or_404(Evento, id=evento_id, usuario=request.user)
    titulo = evento.titulo
    evento.delete()

    Message.objects.create(
        user=request.user,
        content=f"🗑️ Evento eliminado: {titulo}",
        sender_type="event_notification"
    )
    return JsonResponse({"status": "ok"})

@login_required
def verificar_eventos_ajax(request):
    verificar_eventos(request.user)
    return JsonResponse({"status": "ok"})

@login_required
def listar_eventos(request):
    eventos = Evento.objects.filter(usuario=request.user)
    data = [
        {
            "id":          e.id,
            "titulo":      e.titulo,
            "fecha":       e.fecha.isoformat(),
            "descripcion": e.descripcion or "",
            "color":       e.color,
            "categoria":   e.categoria,
        }
        for e in eventos
    ]
    return JsonResponse({"eventos": data})
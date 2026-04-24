from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.db import IntegrityError


from .models import Message, ScheduledMessage, Evento, Estudio, Trabajo, Entretenimiento, Blog, Noticia, Cancion
from .forms import RegistroForm

import random

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

from .utils import programar_mensajes

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
            "title":       e.titulo,
            "start":       e.fecha.isoformat(),
            "description": e.descripcion or "",
            "color":       e.color,
            "categoria":   e.categoria,
        }
        for e in eventos
    ]
    return JsonResponse(data, safe=False)

# ==============================
# 🎵 REPRODUCTOR DE MÚSICA
# ==============================
@login_required
def listar_canciones(request):
    canciones = Cancion.objects.filter(usuario=request.user)
    data = [{"id": c.id, "titulo": c.titulo, "youtube_url": c.youtube_url, "miniatura_url": c.miniatura_url, "duracion": c.duracion} for c in canciones]
    return JsonResponse({"canciones": data})

@login_required
def agregar_cancion(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body) if request.content_type == "application/json" else request.POST
        titulo = data.get("titulo", "Sin título").strip()
        youtube_url = data.get("youtube_url", "").strip()
        
        if not youtube_url:
            return JsonResponse({"status": "error", "error": "El enlace es obligatorio"})

        cancion = Cancion.objects.create(
            usuario=request.user,
            titulo=titulo,
            youtube_url=youtube_url,
            miniatura_url=data.get("miniatura_url", ""),
            duracion=data.get("duracion", "0:00")
        )
        return JsonResponse({"status": "ok", "id": cancion.id})
    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)})

@login_required
def editar_cancion(request, cancion_id):
    if request.method == "POST":
        try:
            cancion = Cancion.objects.get(id=cancion_id, usuario=request.user)
            data = json.loads(request.body)
            cancion.titulo = data.get("titulo", cancion.titulo).strip()
            cancion.save()
            return JsonResponse({"status": "ok"})
        except Cancion.DoesNotExist:
            return JsonResponse({"status": "error", "error": "Canción no encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)})
    return JsonResponse({"status": "error", "error": "Método no permitido"}, status=405)

@login_required
def eliminar_cancion(request, cancion_id):
    if request.method == "POST":
        try:
            cancion = Cancion.objects.get(id=cancion_id, usuario=request.user)
            cancion.delete()
            return JsonResponse({"status": "ok"})
        except Cancion.DoesNotExist:
            return JsonResponse({"status": "error", "error": "Canción no encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)})
    return JsonResponse({"status": "error", "error": "Método no permitido"}, status=405)

# ==============================
# 📝 BLOG
# ==============================
@login_required
def listar_blogs(request):
    blogs = Blog.objects.filter(usuario=request.user)
    data = [{"id": b.id, "titulo": b.titulo, "contenido": b.contenido, "publicado": b.publicado, "fecha": b.creado_en.isoformat()} for b in blogs]
    return JsonResponse({"blogs": data})

@login_required
def crear_blog(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "error": "Método no permitido"}, status=405)
    
    data = json.loads(request.body) if request.content_type == "application/json" else request.POST
    titulo = data.get("titulo", "Nuevo Post").strip()
    contenido = data.get("contenido", "").strip()

    blog = Blog.objects.create(usuario=request.user, titulo=titulo, contenido=contenido)
    return JsonResponse({"status": "ok", "id": blog.id})

# ==============================
# 📚 ESTUDIOS
# ==============================
@login_required
def listar_estudios(request):
    estudios = Estudio.objects.filter(usuario=request.user)
    data = [{"id": e.id, "titulo": e.titulo, "descripcion": e.descripcion, "completado": e.completado} for e in estudios]
    return JsonResponse({"estudios": data})

@login_required
def crear_estudio(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "error": "Método no permitido"}, status=405)
    
    data = json.loads(request.body) if request.content_type == "application/json" else request.POST
    titulo = data.get("titulo", "Nueva Tarea").strip()
    descripcion = data.get("descripcion", "").strip()

    estudio = Estudio.objects.create(usuario=request.user, titulo=titulo, descripcion=descripcion)
    return JsonResponse({"status": "ok", "id": estudio.id})

# ==============================
# 💼 TRABAJOS
# ==============================
@login_required
def listar_trabajos(request):
    trabajos = Trabajo.objects.filter(usuario=request.user)
    data = [{"id": t.id, "titulo": t.titulo, "descripcion": t.descripcion, "completado": t.completado} for t in trabajos]
    return JsonResponse({"trabajos": data})

@login_required
def crear_trabajo(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "error": "Método no permitido"}, status=405)
    
    data = json.loads(request.body) if request.content_type == "application/json" else request.POST
    titulo = data.get("titulo", "Nuevo Proyecto").strip()
    descripcion = data.get("descripcion", "").strip()

    trabajo = Trabajo.objects.create(usuario=request.user, titulo=titulo, descripcion=descripcion)
    return JsonResponse({"status": "ok", "id": trabajo.id})

# ==============================
# 🍿 ENTRETENIMIENTO
# ==============================
@login_required
def listar_entretenimiento(request):
    items = Entretenimiento.objects.filter(usuario=request.user)
    data = [{"id": i.id, "titulo": i.titulo, "tipo": i.tipo, "completado": i.completado} for i in items]
    return JsonResponse({"entretenimiento": data})

@login_required
def crear_entretenimiento(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "error": "Método no permitido"}, status=405)
    
    data = json.loads(request.body) if request.content_type == "application/json" else request.POST
    titulo = data.get("titulo", "Nuevo Juego").strip()
    tipo = data.get("tipo", "juego").strip()

    item = Entretenimiento.objects.create(usuario=request.user, titulo=titulo, tipo=tipo)
    return JsonResponse({"status": "ok", "id": item.id})

@login_required
def toggle_entretenimiento(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Entretenimiento, id=item_id, usuario=request.user)
        item.completado = not item.completado
        item.save()
        return JsonResponse({"status": "ok", "completado": item.completado})
    return JsonResponse({"status": "error"}, status=400)

# ==============================
# 📰 NOTICIAS
# ==============================
@login_required
def listar_noticias(request):
    noticias = Noticia.objects.filter(usuario=request.user)
    data = [{"id": n.id, "titulo": n.titulo, "url": n.url, "fuente": n.fuente, "leida": n.leida} for n in noticias]
    return JsonResponse({"noticias": data})

@login_required
def crear_noticia(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "error": "Método no permitido"}, status=405)
    
    data = json.loads(request.body) if request.content_type == "application/json" else request.POST
    titulo = data.get("titulo", "Nueva Noticia").strip()
    url = data.get("url", "").strip()
    fuente = data.get("fuente", "").strip()

    noticia = Noticia.objects.create(usuario=request.user, titulo=titulo, url=url, fuente=fuente)
    return JsonResponse({"status": "ok", "id": noticia.id})

# ==============================
# 🌤️ CLIMA
# ==============================
import requests

@login_required
def obtener_clima(request):
    usuario = request.user
    ciudad = usuario.ciudad or "Quito"
    
    try:
        # Usamos wttr.in para clima gratuito sin API Key
        url = f"https://wttr.in/{ciudad}?format=j1"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            
            # Mapeo básico de iconos según descripción
            desc_en = current['weatherDesc'][0]['value'].lower()
            icon = "☀️"
            if "cloud" in desc_en: icon = "☁️"
            if "rain" in desc_en: icon = "🌧️"
            if "snow" in desc_en: icon = "❄️"
            if "thunder" in desc_en: icon = "⚡"
            
            weather_data = {
                "temp": current['temp_C'],
                "desc": current['weatherDesc'][0]['value'], # wttr.in a veces no traduce bien, usamos EN por ahora o intentamos ES
                "humidity": current['humidity'],
                "wind": current['windspeedKmph'],
                "city": ciudad,
                "icon": icon
            }
            usuario.clima_cache = weather_data
            usuario.save()
            return JsonResponse(weather_data)
    except Exception as e:
        print(f"Error clima: {e}")
    
    return JsonResponse(usuario.clima_cache or {"temp": "--", "desc": "Cargando...", "icon": "❓", "city": ciudad})

@login_required
def actualizar_ciudad(request):
    if request.method == "POST":
        data = json.loads(request.body)
        nueva_ciudad = data.get("ciudad", "").strip()
        if nueva_ciudad:
            request.user.ciudad = nueva_ciudad
            request.user.save()
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)
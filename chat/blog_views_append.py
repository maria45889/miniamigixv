
# Blog views — appended by script
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Blog
import json


@login_required
def listar_blogs(request):
    blogs = Blog.objects.filter(usuario=request.user).order_by('-creado_en')
    data = [{
        "id": b.id,
        "titulo": b.titulo,
        "contenido": b.contenido,
        "publicado": b.publicado,
        "creado_en": b.creado_en.strftime("%d %b %Y"),
        "actualizado_en": b.actualizado_en.strftime("%d %b %Y"),
    } for b in blogs]
    return JsonResponse({"blogs": data})


@login_required
def crear_blog(request):
    if request.method == "POST":
        data = json.loads(request.body)
        titulo = data.get("titulo", "").strip()
        contenido = data.get("contenido", "").strip()
        if not titulo or not contenido:
            return JsonResponse({"status": "error", "msg": "Titulo y contenido son requeridos"}, status=400)
        blog = Blog.objects.create(
            usuario=request.user,
            titulo=titulo,
            contenido=contenido,
            publicado=data.get("publicado", True)
        )
        return JsonResponse({"status": "ok", "id": blog.id, "creado_en": blog.creado_en.strftime("%d %b %Y")})
    return JsonResponse({"status": "error"}, status=405)


@login_required
def editar_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, usuario=request.user)
    if request.method == "POST":
        data = json.loads(request.body)
        blog.titulo = data.get("titulo", blog.titulo).strip()
        blog.contenido = data.get("contenido", blog.contenido).strip()
        blog.publicado = data.get("publicado", blog.publicado)
        blog.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=405)


@login_required
def eliminar_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, usuario=request.user)
    if request.method == "POST":
        blog.delete()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=405)

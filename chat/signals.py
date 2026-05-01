from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from .models import Message, Evento, Cancion, Blog, Estudio, Trabajo, Entretenimiento, Noticia, Task

@receiver(post_save, sender=Message)
def backup_message_to_mongo(sender, instance, created, **kwargs):
    if created:
        try:
            settings.MONGO_DB.chat_logs.insert_one({
                "type": "message",
                "user_id": instance.user.id,
                "username": instance.user.username,
                "content": instance.content,
                "sender_type": instance.sender_type,
                "timestamp": timezone.now().isoformat(),
                "conversation_id": instance.conversation.id if instance.conversation else None
            })
        except Exception as e:
            print(f"⚠️ Error backup MongoDB (Message): {e}")

@receiver(post_save, sender=Evento)
def backup_event_to_mongo(sender, instance, created, **kwargs):
    try:
        data = {
            "type": "event",
            "user_id": instance.usuario.id,
            "titulo": instance.titulo,
            "fecha": instance.fecha.isoformat() if instance.fecha else None,
            "categoria": instance.categoria,
            "timestamp": timezone.now().isoformat()
        }
        if created:
            settings.MONGO_DB.event_logs.insert_one(data)
        else:
            settings.MONGO_DB.event_logs.update_one(
                {"titulo": instance.titulo, "user_id": instance.usuario.id},
                {"$set": data}
            )
    except Exception as e:
        print(f"⚠️ Error backup MongoDB (Event): {e}")

@receiver(post_save, sender=Blog)
def backup_blog_to_mongo(sender, instance, created, **kwargs):
    try:
        data = {
            "type": "blog",
            "user_id": instance.usuario.id,
            "titulo": instance.titulo,
            "contenido": instance.contenido[:200],
            "timestamp": timezone.now().isoformat()
        }
        if created:
            settings.MONGO_DB.blog_logs.insert_one(data)
        else:
            settings.MONGO_DB.blog_logs.update_one(
                {"titulo": instance.titulo, "user_id": instance.usuario.id},
                {"$set": data}
            )
    except Exception as e:
        print(f"⚠️ Error backup MongoDB (Blog): {e}")

@receiver(post_save, sender=Task)
def backup_task_to_mongo(sender, instance, created, **kwargs):
    try:
        data = {
            "type": "task",
            "user_id": instance.usuario.id,
            "titulo": instance.titulo,
            "completada": instance.completada,
            "timestamp": timezone.now().isoformat()
        }
        if created:
            settings.MONGO_DB.task_logs.insert_one(data)
        else:
            settings.MONGO_DB.task_logs.update_one(
                {"titulo": instance.titulo, "user_id": instance.usuario.id},
                {"$set": data}
            )
    except Exception as e:
        print(f"⚠️ Error backup MongoDB (Task): {e}")

@receiver(post_save, sender=Estudio)
def backup_estudio_to_mongo(sender, instance, created, **kwargs):
    try:
        data = {
            "type": "study",
            "user_id": instance.usuario.id,
            "titulo": instance.titulo,
            "completado": instance.completado,
            "timestamp": timezone.now().isoformat()
        }
        if created:
            settings.MONGO_DB.academic_logs.insert_one(data)
        else:
            settings.MONGO_DB.academic_logs.update_one(
                {"titulo": instance.titulo, "user_id": instance.usuario.id},
                {"$set": data}
            )
    except Exception as e:
        print(f"⚠️ Error backup MongoDB (Study): {e}")

@receiver(post_save, sender=Trabajo)
def backup_trabajo_to_mongo(sender, instance, created, **kwargs):
    try:
        data = {
            "type": "work",
            "user_id": instance.usuario.id,
            "titulo": instance.titulo,
            "completado": instance.completado,
            "timestamp": timezone.now().isoformat()
        }
        if created:
            settings.MONGO_DB.work_logs.insert_one(data)
        else:
            settings.MONGO_DB.work_logs.update_one(
                {"titulo": instance.titulo, "user_id": instance.usuario.id},
                {"$set": data}
            )
    except Exception as e:
        print(f"⚠️ Error backup MongoDB (Work): {e}")

@receiver(post_save, sender=Cancion)
def backup_song_to_mongo(sender, instance, created, **kwargs):
    if created:
        try:
            settings.MONGO_DB.music_logs.insert_one({
                "type": "song",
                "user_id": instance.usuario.id,
                "titulo": instance.titulo,
                "url": instance.youtube_url,
                "timestamp": timezone.now().isoformat()
            })
        except Exception as e:
            print(f"⚠️ Error backup MongoDB (Song): {e}")

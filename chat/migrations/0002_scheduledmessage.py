# Ejecuta esto en tu terminal:
# python manage.py makemigrations chat
# python manage.py migrate
#
# O si prefieres hacerlo manual, crea este archivo en chat/migrations/
# con el número siguiente a tu última migración existente, por ejemplo: 0002_message_recipient.py

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        # Cambia '0001_initial' por el nombre de tu última migración real
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='mensajes_recibidos',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
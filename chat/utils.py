from django.utils import timezone
import random
from .models import Message, ScheduledMessage

CHECKINS = [
    "Oye, ¿cómo estás hoy? 💖 Ya extrañaba saber de ti",
    "¡Hola! Solo pasaba a preguntarte cómo va todo 🌸",
    "¿Cómo te sientes hoy? Cuéntame todo 💕",
    "Hey, hace rato no charlamos... ¿estás bien? 🥺",
]

MOTIVACIONALES = [
    "Recuerda: eres más fuerte de lo que crees 💪✨",
    "Hoy es un buen día para ser feliz 🌟 ¡tú puedes!",
    "No importa cómo salió ayer, hoy es nuevo 💖",
    "Estoy orgullosix de todo lo que has logrado 🎉",
]

BUENOS_DIAS = [
    "¡Buenos días! ☀️ Espero que hoy sea maravilloso para ti 💖",
    "¡Despertaste! 🌸 Un nuevo día lleno de posibilidades te espera",
    "Buenos días 😊 ¿Lista para conquistar el día? ✨",
]

BUENAS_NOCHES = [
    "Buenas noches 🌙 Espero que descanses mucho 💤",
    "Ya es tarde, cuídate y duerme bien 🥺💖",
    "Que tengas dulces sueños esta noche 🌟",
]

MENSAJES_HISTORIAL = {
    "triste": [
        "Oye, noté que últimamente no has estado muy bien 💔 Aquí estoy si quieres hablar",
        "Sé que a veces todo pesa mucho... pero no estás solx 💕",
    ],
    "feliz": [
        "¡Me alegra tanto que hayas estado bien! Sigue brillando ✨💖",
        "Tu energía positiva me contagia 🌸 ¡eres increíble!",
    ],
    "neutral": [
        "Solo quería decirte hola y que pienso en ti 💖",
        "¿Cómo van las cosas por allá? Cuéntame 😊",
    ],
}

def analizar_historial(user):
    ultimos = Message.objects.filter(user=user)\
        .only("content")\
        .order_by('-created_at')[:5]

    textos = " ".join([m.content.lower() for m in ultimos])

    if any(p in textos for p in ["triste", "mal", "lloro", "sola", "solo", "cansada"]):
        return "triste"
    elif any(p in textos for p in ["feliz", "bien", "genial", "contenta", "alegre"]):
        return "feliz"
    
    return "neutral"

def programar_mensajes(user):
    ahora = timezone.localtime(timezone.now())
    hora_actual = ahora.hour
    hoy = ahora.date()

    mensajes = []

    # 🌟 MOTIVACIONAL (1 POR DÍA)
    if not ScheduledMessage.objects.filter(
        user=user,
        tipo='motivacional',
        created_at__date=hoy
    ).exists():
        mensajes.append(ScheduledMessage(
            user=user,
            content=random.choice(MOTIVACIONALES),
            tipo='motivacional',
            programado_para=ahora
        ))

    # 💖 SEGÚN HISTORIAL
    if not ScheduledMessage.objects.filter(
        user=user,
        tipo='historial',
        created_at__date=hoy
    ).exists():
        emocion = analizar_historial(user)
        mensajes.append(ScheduledMessage(
            user=user,
            content=random.choice(MENSAJES_HISTORIAL[emocion]),
            tipo='historial',
            programado_para=ahora
        ))

    # 🌅 SALUDO AUTOMÁTICO
    if not ScheduledMessage.objects.filter(
        user=user,
        tipo='saludo',
        created_at__date=hoy
    ).exists():

        saludo = None

        if 6 <= hora_actual < 12:
            saludo = random.choice(BUENOS_DIAS)

        elif hora_actual >= 21 or hora_actual < 6:
            saludo = random.choice(BUENAS_NOCHES)

        if saludo:
            mensajes.append(ScheduledMessage(
                user=user,
                content=saludo,
                tipo='saludo',
                programado_para=ahora
            ))

    # ⏰ CHECK-IN SI NO HABLA EN 4 HORAS
    ultimo = Message.objects.filter(user=user).order_by('-created_at').first()

    if ultimo:
        horas = (ahora - ultimo.created_at).total_seconds() / 3600
    else:
        horas = 99  # si no hay mensajes

    if horas > 4 and not ScheduledMessage.objects.filter(
        user=user,
        tipo='checkin',
        created_at__date=hoy
    ).exists():

        mensajes.append(ScheduledMessage(
            user=user,
            content=random.choice(CHECKINS),
            tipo='checkin',
            programado_para=ahora
        ))

    # 💾 GUARDAR TODO JUNTO (OPTIMIZADO)
    if mensajes:
        ScheduledMessage.objects.bulk_create(mensajes)
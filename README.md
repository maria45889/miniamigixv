<div align="center">

# 💖 MiniAmigixV: Ultimate Hybrid FullStack Edition

### 🌟 Centro de mando personal diseñado con Django 6 + PostgreSQL + MongoDB + API Rest

<img src="static/chat/img/logo.png" width="200px" style="border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);" alt="MiniAmigixV Logo"/>

<br>

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-6.0-green?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-🐘-blue?style=for-the-badge&logo=postgresql)
![MongoDB](https://img.shields.io/badge/MongoDB-🍃-green?style=for-the-badge&logo=mongodb)
![API](https://img.shields.io/badge/API_Rest-Postman_Ready-orange?style=for-the-badge)

</div>

---

# ✨ Arquitectura Híbrida de Vanguardia

**MiniAmigixV** utiliza un sistema de almacenamiento dual para maximizar el rendimiento y la seguridad:

*   **🐘 PostgreSQL (Relacional)**: Maneja el corazón de la aplicación (Usuarios, Eventos, Blogs, Tareas). Es el motor de la consistencia y la integridad de tus datos.
*   **🍃 MongoDB (NoSQL)**: Actúa como nuestra **Bóveda de Respaldo Infinita**. Cada mensaje de chat se sincroniza automáticamente con MongoDB para asegurar que tu historial sea eterno y escalable.

---

# 🚀 Características de Élite

### 📡 FullStack API (Mobile Ready)
*   **Django Rest Framework**: Integración de una arquitectura de API profesional.
*   **Postman Collection**: Kit de pruebas incluido para controlar tu dashboard desde cualquier herramienta externa.
*   **CORS Enabled**: Configuración lista para conectar con **Android Studio**.

### ✍️ Mi Blog Personal
*   **Módulo de Escritura**: Un espacio elegante para inmortalizar tus pensamientos, con gestión total y persistencia en PostgreSQL.

### 🎨 Identidad & Branding
*   **Logo Personalizado**: Sidebar con branding oficial y efectos de iluminación dinámica.
*   **Avatar System**: Cambia tu foto de perfil y la de tu Chat usando URLs personalizadas.

---

# 🛠 Stack Tecnológico

| Tecnología | Rol |
|-----------|------|
| **Django 6.0** | Framework de alto rendimiento |
| **PostgreSQL** | Motor SQL para datos estructurados |
| **MongoDB** | Motor NoSQL para almacenamiento masivo de mensajes |
| **DRF** | Motor de API Restful |
| **Psycopg 3** | Adaptador moderno de base de datos |
| **CSS3 & JS ES14** | Interfaz Glassmorphism y lógica dinámica |

---

# ⚙ Instalación Pro

```bash
# 1. Clonar e instalar
git clone https://github.com/maria45889/miniamigixv.git
cd miniamigixv
pip install -r requirements.txt

# 2. Configurar Bases de Datos
# Configura PostgreSQL (pgAdmin) y MongoDB en tu .env
python manage.py migrate

# 3. ¡Desplegar Magia!
python manage.py runserver
```

---

## 🗨️ Chat Interactivo

El módulo **Chat** permite conversar con tu asistente virtual personal, almacenar mensajes en tiempo real y sincronizarlos con MongoDB para persistencia infinita.  
### ¿Para qué sirve?
- **Asistente personal**: Responde preguntas, guarda notas y ejecuta comandos simples.
- **Comunicación en tiempo real**: Interfaz con actualizaciones instantáneas usando websockets/Django Channels.
- **Almacenamiento robusto**: Cada mensaje se guarda tanto en la base relacional como en la NoSQL para recuperación y análisis posterior.
### Requisitos
- **MongoDB** corriendo y configurado en `.env` (`MONGODB_URI`).
- **Django Channels** instalado (`pip install channels channels_redis`).
- **Redis** como broker para los sockets (opcional pero recomendado).

### Cómo probarlo
1. Asegúrate de haber ejecutado `python manage.py migrate` y configurado la base de datos.  
2. Inicia el servidor con `python manage.py runserver`.  
3. Abre `http://127.0.0.1:8000/chat/` y escribe un mensaje.  

El chat mostrará los mensajes anteriores y los nuevos aparecerán al instante.  

---

<div align="center">
<b>MiniAmigixV v3.5 (Hybrid Edition)</b> - Potencia relacional y flexibilidad NoSQL.
</div>

---

## 📦 Uso rápido del Chat

```bash
# Inicia el servidor
python manage.py runserver
# Abre la URL del chat
http://127.0.0.1:8000/chat/
```

Escribe cualquier mensaje y verás la respuesta del asistente en tiempo real.

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Sigue estos pasos:
1. Haz fork del repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Implementa los cambios y escribe pruebas.
4. Haz commit y push a tu fork.
5. Abre un Pull Request.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
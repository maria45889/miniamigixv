// ==============================
// 🎯 ELEMENTOS
// ==============================
const calendarEl       = document.getElementById("calendar");
const form             = document.getElementById("chat-form");
const input            = document.getElementById("message-input");
const chatBox          = document.getElementById("chat-box");
const darkBtn          = document.getElementById("dark-btn");
const relojEl          = document.getElementById("reloj");
const fechaEl          = document.getElementById("fecha");
const addEventBtn      = document.getElementById("add-event-btn");
const eventModal       = document.getElementById("event-modal");
const closeModal       = document.getElementById("close-modal");
const eventForm        = document.getElementById("event-form");
const editModal        = document.getElementById("edit-modal");
const closeEditModal   = document.getElementById("close-edit-modal");
const editForm         = document.getElementById("edit-form");

let enviando = false;
let calendar  = null;

// ==============================
// 🔐 CSRF
// ==============================
function getCsrf() {
    const el = document.querySelector("[name=csrfmiddlewaretoken]");
    return el ? el.value : "";
}

// ==============================
// 🧠 FETCH SEGURO (MEJORADO)
// ==============================
async function fetchSeguro(url, options = {}) {
    try {
        const res = await fetch(url, options);

        if (!res.ok) {
            console.error("❌ Error HTTP:", res.status);
            return null;
        }

        const contentType = res.headers.get("content-type");

        if (contentType && contentType.includes("application/json")) {
            return await res.json();
        } else {
            console.warn("⚠️ Respuesta no es JSON");
            return null;
        }

    } catch (e) {
        console.error("❌ Error de conexión:", e);
        return null;
    }
}

// ==============================
// ⏰ RELOJ
// ==============================
function actualizarReloj() {
    if (!relojEl || !fechaEl) return;

    const now = new Date();
    relojEl.textContent = now.toLocaleTimeString('es-EC');
    fechaEl.textContent = now.toLocaleDateString('es-EC', {
        weekday: 'long',
        day: 'numeric',
        month: 'long',
        year: 'numeric'
    });
}

setInterval(actualizarReloj, 1000);
actualizarReloj();

// ==============================
// 🌙 DARK MODE
// ==============================
if (darkBtn) {
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark");
    }

    darkBtn.onclick = () => {
        document.body.classList.toggle("dark");
        localStorage.setItem("darkMode", document.body.classList.contains("dark"));
    };
}

// ==============================
// 💬 CHAT
// ==============================
function scrollBottom() {
    if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
}

function addMessage(text, type) {
    if (!chatBox) return;

    const div = document.createElement("div");
    div.className = `message ${type}`;

    const now = new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
    });

    div.innerHTML = `
        <div>${text}</div>
        <div class="meta">${now}</div>
    `;

    chatBox.appendChild(div);
    scrollBottom();
}

function mostrarTyping() {
    if (!chatBox || document.getElementById("typing")) return;

    const t = document.createElement("div");
    t.className = "typing";
    t.id = "typing";
    t.innerHTML = '<span></span><span></span><span></span>';

    chatBox.appendChild(t);
}

function quitarTyping() {
    const t = document.getElementById("typing");
    if (t) t.remove();
}

// ==============================
// 🔊 VOZ
// ==============================
function hablar(texto) {
    if (!texto) return;

    const msg = new SpeechSynthesisUtterance(texto);
    msg.lang = "es-ES";

    speechSynthesis.cancel();
    speechSynthesis.speak(msg);
}

// ==============================
// 🚀 ENVIAR MENSAJE (OPTIMIZADO)
// ==============================
if (form && input) {
    form.addEventListener("submit", async e => {
        e.preventDefault();

        if (enviando) return;

        const msg = input.value.trim();
        if (!msg) return;

        enviando = true;

        addMessage(msg, "user");
        input.value = "";
        mostrarTyping();

        const data = await fetchSeguro("/send_message/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCsrf()
            },
            body: new URLSearchParams({ message: msg })
        });

        quitarTyping();

        if (!data) {
            addMessage("Error del servidor 😢", "bot");
            enviando = false;
            return;
        }

        addMessage(data.reply, "bot");

        if (data.audio_url) {
            new Audio(data.audio_url).play().catch(() => hablar(data.reply));
        } else {
            hablar(data.reply);
        }

        enviando = false;
    });
}

// ==============================
// ➕ MODAL EVENTO
// ==============================
if (addEventBtn && eventModal && closeModal) {
    addEventBtn.onclick = () => eventModal.classList.add("active");
    closeModal.onclick = () => eventModal.classList.remove("active");
}

// ==============================
// 💾 CREAR EVENTO
// ==============================
if (eventForm) {
    eventForm.addEventListener("submit", async e => {
        e.preventDefault();

        const data = await fetchSeguro("/eventos/crear/", {
            method: "POST",
            headers: { "X-CSRFToken": getCsrf() },
            body: new URLSearchParams(new FormData(eventForm))
        });

        if (data?.status === "ok") {
            eventModal.classList.remove("active");
            eventForm.reset();
            await recargarCalendario();
        } else {
            alert("Error al crear evento 😢");
        }
    });
}

// ==============================
// ✏️ EDITAR EVENTO
// ==============================
document.addEventListener("click", e => {
    if (!e.target.matches(".btn-edit")) return;

    if (!editModal || !editForm) return;

    const btn = e.target;

    document.getElementById("edit-evento-id").value = btn.dataset.id;
    document.getElementById("edit-titulo").value = btn.dataset.titulo;
    document.getElementById("edit-descripcion").value = btn.dataset.descripcion;
    document.getElementById("edit-fecha").value = btn.dataset.fecha;
    document.getElementById("edit-recordatorio").checked = btn.dataset.recordatorio === "true";

    editModal.classList.add("active");
});

if (closeEditModal) {
    closeEditModal.onclick = () => editModal.classList.remove("active");
}

if (editForm) {
    editForm.addEventListener("submit", async e => {
        e.preventDefault();

        const id = document.getElementById("edit-evento-id").value;

        const data = await fetchSeguro(`/eventos/editar/${id}/`, {
            method: "POST",
            headers: { "X-CSRFToken": getCsrf() },
            body: new URLSearchParams(new FormData(editForm))
        });

        if (data?.status === "ok") {
            editModal.classList.remove("active");
            await recargarCalendario();
        } else {
            alert("Error al editar 😢");
        }
    });
}

// ==============================
// 🗑️ ELIMINAR EVENTO
// ==============================
document.addEventListener("click", async e => {
    if (!e.target.matches(".btn-delete")) return;

    const id = e.target.dataset.id;

    if (!confirm("¿Eliminar evento? 💔")) return;

    const data = await fetchSeguro(`/eventos/eliminar/${id}/`, {
        method: "POST",
        headers: { "X-CSRFToken": getCsrf() }
    });

    if (data?.status === "ok") {
        await recargarCalendario();
    } else {
        alert("Error al eliminar 😢");
    }
});

// ==============================
// 🔔 VERIFICAR EVENTOS (OPTIMIZADO)
// ==============================
// ⛔ Antes: cada 60s → saturaba ngrok
// ✅ Ahora: cada 2 minutos
setInterval(async () => {
    await fetchSeguro("/eventos/verificar/", {
        method: "POST",
        headers: { "X-CSRFToken": getCsrf() }
    });
}, 120000);

// ==============================
// 📅 FULLCALENDAR
// ==============================
function initCalendar(eventos) {
    if (!calendarEl) return;

    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: eventos
    });

    calendar.render();
}

async function recargarCalendario() {
    if (!calendar) return;

    const data = await fetchSeguro("/eventos/listar/");

    if (!data?.eventos) return;

    calendar.removeAllEvents();

    data.eventos.forEach(ev => {
        calendar.addEvent({
            id: ev.id,
            title: ev.titulo,
            start: ev.fecha,
            description: ev.descripcion
        });
    });
}
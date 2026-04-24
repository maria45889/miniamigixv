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
// 🧠 FETCH SEGURO (OPTIMIZADO PARA JSON)
// ==============================
async function fetchSeguro(url, options = {}) {
    try {
        const res = await fetch(url, options);
        if (!res.ok) return null;
        
        const contentType = res.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            return await res.json();
        }
        return null;
    } catch (e) {
        console.error("❌ Error:", e);
        return null;
    }
}

// ==============================
// ⏰ RELOJ & FECHA
// ==============================
function actualizarReloj() {
    if (!relojEl || !fechaEl) return;
    const now = new Date();
    relojEl.textContent = now.toLocaleTimeString('es-EC', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    fechaEl.textContent = now.toLocaleDateString('es-EC', { weekday: 'long', day: 'numeric', month: 'long' });
}
setInterval(actualizarReloj, 1000);
actualizarReloj();

// ==============================
// 🌙 MODO OSCURO
// ==============================
if (darkBtn) {
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark-theme");
        darkBtn.textContent = '☀️';
    }
    darkBtn.onclick = () => {
        document.body.classList.toggle("dark-theme");
        const isDark = document.body.classList.contains("dark-theme");
        darkBtn.textContent = isDark ? '☀️' : '🌙';
        localStorage.setItem("darkMode", isDark);
    };
}

// ==============================
// 💬 CHAT IA
// ==============================
function scrollBottom() { if (chatBox) chatBox.scrollTop = chatBox.scrollHeight; }

function addMessage(text, type) {
    if (!chatBox) return;
    const div = document.createElement("div");
    div.style.cssText = `max-width: 80%; padding: 12px 16px; border-radius: 16px; font-size: 0.95rem; margin-bottom: 10px; ${type === 'user' ? 'align-self: flex-end; background: var(--acc-purple); color: #000;' : 'align-self: flex-start; background: rgba(255,255,255,0.05); border: 1px solid var(--bdr);'}`;
    div.textContent = text;
    chatBox.appendChild(div);
    scrollBottom();
}

if (form && input) {
    form.addEventListener("submit", async e => {
        e.preventDefault();
        const msg = input.value.trim();
        if (enviando || !msg) return;

        enviando = true;
        addMessage(msg, "user");
        input.value = "";

        const data = await fetchSeguro("/chat/send/", { // Ajustado a la ruta común
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRFToken": getCsrf() },
            body: JSON.stringify({ content: msg })
        });

        if (data && data.reply) {
            addMessage(data.reply, "bot");
            if (window.speechSynthesis) {
                const utt = new SpeechSynthesisUtterance(data.reply);
                utt.lang = 'es-ES';
                speechSynthesis.speak(utt);
            }
        } else {
            addMessage("Algo salió mal... 😢", "bot");
        }
        enviando = false;
    });
}

// ==============================
// 📅 EVENTOS & CALENDARIO
// ==============================
if (addEventBtn) addEventBtn.onclick = () => eventModal.classList.add("active");
if (closeModal) closeModal.onclick = () => eventModal.classList.remove("active");

async function initCalendar() {
    if (!calendarEl) return;
    const data = await fetchSeguro("/eventos/listar/");
    const eventos = data ? data.eventos.map(ev => ({ id: ev.id, title: ev.titulo, start: ev.fecha, color: ev.color })) : [];

    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: { left: 'prev,next today', center: 'title', right: '' },
        events: eventos,
        height: 'auto'
    });
    calendar.render();
}

document.addEventListener('DOMContentLoaded', initCalendar);

// ==============================
// 🗑️ ELIMINAR EVENTO (Delegación)
// ==============================
document.addEventListener("click", async e => {
    const btn = e.target.closest(".btn-delete");
    if (!btn) return;
    if (!confirm("¿Borrar este evento? 💔")) return;

    const res = await fetch(`/eventos/eliminar/${btn.dataset.id}/`, {
        method: "POST",
        headers: { "X-CSRFToken": getCsrf() }
    });
    if (res.ok) location.reload();
});
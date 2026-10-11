// Minimal chat client. POSTs to /api/chat (the Pages Function) and appends
// the reply to the message list.

const form = document.getElementById("form");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const messages = document.getElementById("messages");
const statusEl = document.getElementById("status");

const THREAD_ID = "web-user-" + Math.random().toString(36).slice(2, 10);

function appendMessage(role, text) {
  const li = document.createElement("li");
  li.className = `msg msg--${role}`;
  li.textContent = text;
  messages.appendChild(li);
  messages.scrollTop = messages.scrollHeight;
  return li;
}

function setStatus(text) {
  statusEl.textContent = text;
}

function setBusy(busy) {
  sendBtn.disabled = busy;
  input.disabled = busy;
  sendBtn.textContent = busy ? "Thinking..." : "Send";
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  appendMessage("user", message);
  input.value = "";
  setBusy(true);
  setStatus("");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ message, thread_id: THREAD_ID }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      const detail = data?.error || `HTTP ${res.status}`;
      appendMessage("assistant", `Error: ${detail}`);
      setStatus(detail);
      return;
    }
    appendMessage("assistant", data.reply || "(empty reply)");
  } catch (err) {
    appendMessage("assistant", `Network error: ${err.message}`);
    setStatus(err.message);
  } finally {
    setBusy(false);
    input.focus();
  }
});
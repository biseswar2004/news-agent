// Set today's date in topbar
document.addEventListener("DOMContentLoaded", () => {
  const now = new Date();
  const options = { weekday:'long', year:'numeric', month:'long', day:'numeric' };
  const dateEl = document.getElementById("topbarDate");
  if (dateEl) dateEl.textContent = now.toLocaleDateString('en-IN', options);
  checkStatus();
});

async function checkStatus() {
  try {
    const res = await fetch("/api/status");
    const data = await res.json();
    const el = document.getElementById("topbarStatus");
    if (el) {
      el.textContent = data.briefing_ready
        ? "● Briefing Ready"
        : "● No briefing yet";
    }
  } catch(e) {}
}

async function runNow() {
  const btn = document.getElementById("runBtn");
  const icon = document.getElementById("runIcon");
  const text = document.getElementById("runText");

  btn.disabled = true;
  icon.innerHTML = '<span class="spinner"></span>';
  text.textContent = "Starting...";

  try {
    const res = await fetch("/api/run", { method: "POST" });
    const data = await res.json();

    if (data.status === "success") {
      // Show success immediately — don't wait
      icon.textContent = "✓";
      text.textContent = "Running in background!";
      showToast("⚡ Briefing running! Check Telegram in 2-3 min.", "success");

      // Reload page after 3 minutes to show result
      setTimeout(() => location.reload(), 180000);

      // Re-enable button after 10 seconds
      setTimeout(() => {
        btn.disabled = false;
        icon.textContent = "⚡";
        text.textContent = "Run Briefing";
      }, 10000);

    } else {
      showToast("✗ " + data.message, "error");
      btn.disabled = false;
      icon.textContent = "⚡";
      text.textContent = "Run Briefing";
    }
  } catch(e) {
    showToast("✗ Network error", "error");
    btn.disabled = false;
    icon.textContent = "⚡";
    text.textContent = "Run Briefing";
  }
}

async function saveSettings() {
  const name = document.getElementById("name")?.value;
  const topics = document.getElementById("topics")?.value;
  const telegramId = document.getElementById("telegramId")?.value;

  if (!name?.trim()) { showToast("✗ Name cannot be empty", "error"); return; }

  try {
    const res = await fetch("/api/save-settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, topics, telegramId })
    });
    const data = await res.json();
    if (data.status === "success") {
      showToast("✓ Settings saved!", "success");
      const el = document.getElementById("saveStatus");
      if (el) el.textContent = "✓ Saved successfully";
    }
  } catch(e) {
    showToast("✗ Error saving", "error");
  }
}

function copyScript() {
  const text = document.getElementById("scriptText")?.textContent;
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    showToast("✓ Script copied!", "success");
  });
}

function toggleCard(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.style.display = el.style.display === "none" ? "block" : "none";
}

function showToast(message, type) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = message;
  toast.className = `toast ${type} show`;
  setTimeout(() => toast.classList.remove("show"), 3000);
}
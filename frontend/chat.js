const baseUrl =
  window.location.hostname.includes("localhost") ||
  window.location.hostname.includes("127.0.0.1")
    ? ""
    : "https://supportplaymaker.onrender.com";

async function sendMessage() {
  const input = document.getElementById("message-input");
  const chatBox = document.getElementById("chat-box");
  const message = input.value.trim();
  if (!message) return;

  // Display user message
  chatBox.innerHTML += `<div class="user"><strong>You:</strong> ${message}</div>`;
  input.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const res = await fetch(`${baseUrl}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: "demo-user",
        message,
        metadata: {},
      }),
    });

    const data = await res.json();
    const reply = data.response || "Sorry, something went wrong.";
    chatBox.innerHTML += `<div class="bot"><strong>Agent:</strong> ${reply}</div>`;
  } catch (err) {
    chatBox.innerHTML += `<div class="bot"><strong>Agent:</strong> Failed to connect to server.</div>`;
  }

  chatBox.scrollTop = chatBox.scrollHeight;
}

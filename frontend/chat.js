async function sendMessage() {
  const input = document.getElementById("message-input");
  const chatBox = document.getElementById("chat-box");
  const message = input.value.trim();
  if (!message) return;

  // Display user message
  chatBox.innerHTML += `<div class="user"><strong>You:</strong> ${message}</div>`;
  input.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;

  // Call the backend
  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: "demo-user",
      message,
      metadata: {}
    })
  });

  const data = await res.json();
  const reply = data.response || "Sorry, something went wrong.";

  // Display bot reply
  chatBox.innerHTML += `<div class="bot"><strong>Agent:</strong> ${reply}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}

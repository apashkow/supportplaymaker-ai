document.addEventListener("DOMContentLoaded", function () {
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  sendBtn.addEventListener("click", async function () {
    const userMessage = userInput.value.trim();
    if (!userMessage) return;

    appendMessage("You", userMessage);
    userInput.value = "";

    try {
      const response = await fetch("https://supportplaymaker.onrender.com/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_id: "user-001",
          message: userMessage,
          metadata: {}
        })
      });

      if (!response.ok) throw new Error("Server error");

      const data = await response.json();
      appendMessage("Agent", data.reply || "No response.");
    } catch (error) {
      appendMessage("Agent", "❌ Failed to connect to server.");
      console.error(error);
    }
  });

  function appendMessage(sender, message) {
    const messageEl = document.createElement("div");
    messageEl.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(messageEl);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
});

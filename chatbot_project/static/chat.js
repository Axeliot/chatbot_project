function sendMessage() {
  const input = document.getElementById("msg-input");
  const message = input.value.trim();

  if (!message) return;

  fetch("/chat", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  })
  .then(res => res.json())
  .then(data => {
    const box = document.getElementById("chat-box");

    // ✅ Use marked to convert bot response from markdown to HTML
    const botHtml = marked.parse(data.response);

    box.innerHTML += `
      <div class="chat-entry">
        <div class="user">You:</div><div>${message}</div>
        <div class="bot">Bot:</div><div>${botHtml}</div>
      </div>
    `;
    box.scrollTop = box.scrollHeight;
    input.value = "";
  })
  .catch(err => {
    alert("Something went wrong. Check console.");
    console.error(err);
  });
}

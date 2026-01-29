async function send(event) {
  event.preventDefault();
  const msg = document.getElementById("msg").value;
  const chat = document.getElementById("chat");

  if (!msg.trim()) return;

  chat.innerHTML += `<p><b>You:</b> ${msg}</p>`;

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: msg})
    });

    const data = await res.json();
    chat.innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
  } catch (error) {
    chat.innerHTML += `<p><b>Error:</b> ${error.message}</p>`;
  }

  document.getElementById("msg").value = "";
}
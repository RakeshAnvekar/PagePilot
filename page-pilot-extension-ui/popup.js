const chat = document.getElementById("chat");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

let pageData = {
  url: "",
  content: ""
};

/* 🔹 On popup open → read page content */
document.addEventListener("DOMContentLoaded", async () => {
  const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  chrome.tabs.sendMessage(
    tab.id,
    { type: "READ_PAGE_CONTENT" },
    (response) => {
      if (!response) {
        addMessage("ai", "Unable to read this page.");
        return;
      }

      pageData.url = response.url;
      pageData.content = response.content;

      console.log("URL:", pageData.url);
      console.log("Content length:", pageData.content.length);

      addMessage("ai", "Page loaded. Ask your question.");
    }
  );
});

/* 🔹 Ask button */
sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});

function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage("user", text);
  input.value = "";

  
  fetch("http://127.0.0.1:8000/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      url: pageData.url,
      content: pageData.content,
      question: text
    })
  })
    .then(res => res.json())
    .then(data => {
      addMessage("ai", data.answer);
    })
    .catch(err => {
      console.error(err);
      addMessage("ai", "Error connecting to AI service.");
    });
}

function addMessage(type, text) {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.innerText = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

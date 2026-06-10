const askBtn = document.getElementById("askBtn");
const questionInput = document.getElementById("question");
const chatArea = document.getElementById("chatArea");
const emptyState = document.getElementById("emptyState");
const clearBtn = document.getElementById("clearBtn");
const statusDot = document.getElementById("statusDot");

// Press Enter to send
questionInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") askBtn.click();
});

clearBtn.addEventListener("click", () => {
  chatArea.innerHTML = '';
  chatArea.appendChild(emptyState);
  emptyState.style.display = "flex";
});

function addMessage(text, role) {
  emptyState.style.display = "none";

  const msg = document.createElement("div");
  msg.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerText = text;

  msg.appendChild(bubble);
  chatArea.appendChild(msg);
  chatArea.scrollTop = chatArea.scrollHeight;
  return bubble;
}

function addThinking() {
  emptyState.style.display = "none";

  const msg = document.createElement("div");
  msg.className = "message bot";

  const bubble = document.createElement("div");
  bubble.className = "bubble thinking";
  bubble.innerHTML = `<div class="dots"><span></span><span></span><span></span></div>`;

  msg.appendChild(bubble);
  chatArea.appendChild(msg);
  chatArea.scrollTop = chatArea.scrollHeight;
  return msg;
}

askBtn.addEventListener("click", async () => {
  const question = questionInput.value.trim();
  if (!question) return;

  questionInput.value = "";
  addMessage(question, "user");

  const thinkingMsg = addThinking();
  statusDot.style.background = "#f59e0b";
  statusDot.style.boxShadow = "0 0 6px #f59e0b88";

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => document.body.innerText
    });

    const page_text = results[0].result;

    const response = await fetch("https://web-chatbot-2lhr.onrender.com", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        page_text: page_text,
        question: question,
        session_id: "user_session_1"
      })
    });

    const data = await response.json();
    thinkingMsg.remove();
    addMessage(data.answer, "bot");

    statusDot.style.background = "#22c55e";
    statusDot.style.boxShadow = "0 0 6px #22c55e88";

  } catch (err) {
    thinkingMsg.remove();
    addMessage("Something went wrong. Make sure the backend is running.", "bot");

    statusDot.style.background = "#ef4444";
    statusDot.style.boxShadow = "0 0 6px #ef444488";
  }
});
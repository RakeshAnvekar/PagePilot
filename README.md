# AI Page Reader – Browser-Based Contextual AI Assistant

AI Page Reader is a **browser extension + Python AI backend** that allows users to ask questions about **any web page they are currently viewing**.
The AI answers **only from the page content**, remembers the conversation context, and **never hallucinates**.

---

## 🚀 What Problem Does This Solve?

Users often need to:
- Understand product pages quickly
- Ask questions about company documentation
- Summarize long articles
- Get clarity without copying content into another tool

**AI Page Reader solves this by bringing AI directly into the browser, scoped to the current page.**

---

## 🧠 Key Capabilities

- 📄 Reads **real, rendered page content** (including dynamic & authenticated pages)
- 💬 Chat-style interface inside the browser
- 🧠 Remembers conversation context (multi-turn)
- ✅ Answers **only from the page**
- ❌ Clearly says *"The result for your question is not available"* when info is missing
- 🔐 Secure (AI keys never exposed to browser)
- 🧩 Extensible (RAG, real-time data, tools)

---

## 🧩 High-Level Flow

```
User on Web Page
        ↓
Clicks AI Extension
        ↓
AI Reads Page Content
        ↓
User Asks Question
        ↓
AI Uses Context
        ↓
AI Answers from Page
```

---

## 🏗️ Project Structure

```
PAGE-READER/
│
├── page-reader-core/            # Python AI Backend
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
└── page-reader-extension-ui/    # Browser Extension (UI + DOM reader)
    ├── manifest.json
    ├── content.js
    ├── popup.html
    ├── popup.css
    └── popup.js
```

---

## 🌐 Architecture Overview

- **Browser Extension**
  - Reads the page DOM using a content script
  - Shows a chat UI
  - Sends page content + user questions to backend

- **Python Backend (FastAPI)**
  - Manages AI calls
  - Maintains conversation memory (per page)
  - Applies strict guardrails (no hallucination)
  - Returns clean JSON responses

---

## 🔐 Security & Compliance

- No server-side scraping
- No AI API keys in browser
- Uses user-authorized browser session
- Works on internal, authenticated, and dynamic pages

---

## ⚙️ Setup Instructions

### Backend (Python)

```bash
cd page-reader-core
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

Verify backend:
```
http://127.0.0.1:8000/docs
```

---

### Browser Extension

1. Open Chrome
2. Go to `chrome://extensions`
3. Enable **Developer Mode**
4. Click **Load unpacked**
5. Select `page-reader-extension-ui/`

---

## 🧪 Example Questions

- What is this page about?
- Who is this product for?
- Summarize this page
- Is pricing mentioned?
- Explain that in simple terms

If the information is not on the page, the AI responds with:

> **The result for your question is not available.**

---

## 🚀 Future Enhancements

- Chunking for large pages
- RAG with vector databases
- Real-time tools (stocks, weather)
- Persistent memory (Redis / DB)
- Answer citations and highlights

---
UI
<img width="1248" height="927" alt="image" src="https://github.com/user-attachments/assets/74b90bfc-72a2-4949-a548-552c81732406" />

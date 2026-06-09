# 🤖 Web Page Chatbot — Chrome Extension

A RAG-based Chrome Extension that lets you chat with any webpage. Ask questions about the current page and get answers based on its content — powered by LangChain, FAISS, and Qwen 2.5-72B.

## How It Works

1. User opens the extension on any webpage
2. Extension captures the page text automatically
3. Text is chunked and embedded using BAAI/bge-small-en-v1.5
4. Stored in a FAISS vector database
5. User asks a question → relevant chunks are retrieved
6. Qwen 2.5-72B generates an answer based only on retrieved context
7. Chat history is maintained per session

## Tech Stack

- **Backend** — Django, Django REST Framework
- **AI/RAG** — LangChain, FAISS, HuggingFace
- **Embeddings** — BAAI/bge-small-en-v1.5
- **LLM** — Qwen 2.5-72B-Instruct
- **Frontend** — Chrome Extension (HTML, CSS, JS)

## Project Structure
web-chatbot/
├── backend/
│   ├── views.py        # RAG pipeline + chat history
│   ├── urls.py
│   └── settings.py
├── chrome-extension/
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js
├── .env
├── requirements.txt
└── README.md

## Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/ayangithub00/Web-Chatbot-.git
cd Web-Chatbot-
```

### 2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your HuggingFace API key in `.env`
HUGGINGFACEHUB_API_TOKEN=your_token_here

### 5. Run Django server
```bash
python manage.py runserver
```

### 6. Load Chrome Extension
- Open `chrome://extensions`
- Enable **Developer Mode**
- Click **Load Unpacked**
- Select the `chrome-extension/` folder

### 7. Use it
- Go to any webpage
- Click the extension icon
- Ask anything about the page

## Author

**Ayan Islam**  
[GitHub](https://github.com/ayangithub00) · [LinkedIn](https://linkedin.com/in/ayan-islam-5a0212237)
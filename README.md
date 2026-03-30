# 🤖 AI Q&A Assistant

A simple AI Q&A application with multi-turn chat history and streaming responses, built using **LangChain**, **Groq**, and **Streamlit**.

---

## Features

- 💬 Multi-turn conversational chat with memory
- ⚡ Streaming responses via Groq (Qwen 3 32B)
- 🔑 API key stored securely in `.env` file
- 🗑️ Clear chat history anytime
- 🧱 Clean, modular code structure

---

## Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| UI         | Streamlit               |
| LLM        | Qwen 3 32B via Groq    |
| Framework  | LangChain               |
| Language   | Python 3.9+             |

---

## Project Structure

```
ai-qa-app/
├── app.py              # Streamlit UI & chat logic
├── qa_chain.py         # LangChain + Groq chain setup
├── config.py           # Model config, loads env vars
├── .env                # Your API key (never commit this)
├── .env.example        # Edit this file for groq_api_key
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup & Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up your API key

Copy the example env file and add your key:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

Get a free key at [console.groq.com](https://console.groq.com) → API Keys.

### 3. Run the app

```bash
streamlit run app.py
```

App opens at `http://localhost:8501` and starts the chat session directly.

---

## How It Works

1. App loads the Groq API key from `.env` on startup
2. User types a question in the chat input
3. The full conversation history is passed as context with each request
4. The LangChain chain streams the response token by token via `st.write_stream`
5. Response is saved to session state for future context

---

## Configuration

Edit `config.py` to change:
- `GROQ_MODEL` — swap to any Groq-supported model
- `TEMPERATURE` — control response creativity (0.0–1.0)
- `MAX_TOKENS` — limit response length
- `SYSTEM_MSG` — customize the assistant's personality
- `MAX_CHAT_HISTORY` — number of past messages to include as context

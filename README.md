# FastAPI Streaming - AI Research Analyst

API backend untuk AI Research Analyst yang bisa menganalisis perusahaan dan saham secara real-time dengan streaming response.

## Fitur

- Streaming chat response menggunakan Server-Sent Events (SSE)
- Pencarian web menggunakan Tavily
- Data saham real-time menggunakan yFinance
- Session management untuk percakapan
- API docs dengan Scalar (`/scalar`)

## Tech Stack

- **FastAPI** - Web framework
- **OpenAI Agents SDK** + **LiteLLM** - AI agent dengan tool calling
- **SQLModel** + **aiosqlite** - Database (SQLite async)
- **Tavily** - Web search API
- **yFinance** - Stock market data

## Setup

1. Clone repository dan install dependencies:

```bash
uv sync
```

2. Buat file `.env`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

3. Jalankan server:

```bash
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/chat-session/` | Buat session baru |
| POST | `/chat/` | Kirim pesan dan terima streaming response |
| GET | `/scalar` | API documentation |

## Contoh Request

### Buat Session

```bash
curl -X POST http://localhost:8000/chat-session/
```

### Kirim Pesan

```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"session_id": "1", "message": "Analisis saham AAPL"}'
```

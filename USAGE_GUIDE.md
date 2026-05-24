# Panduan Penggunaan Agen AI Inaproc

## 📖 Daftar Isi
1. [Instalasi](#instalasi)
2. [Konfigurasi](#konfigurasi)
3. [Menjalankan Aplikasi](#menjalankan-aplikasi)
4. [Menggunakan API](#menggunakan-api)
5. [Contoh Penggunaan](#contoh-penggunaan)
6. [Troubleshooting](#troubleshooting)

---

## Instalasi

### 1. Prerequisites
Pastikan Anda memiliki:
- Python 3.9 atau lebih tinggi
- Git
- OpenAI API Key (dari https://platform.openai.com)
- (Optional) Docker dan Docker Compose

### 2. Clone Repository
```bash
git clone https://github.com/agnijayamandiri2026-cmd/Agen-AI-Inaproc.git
cd Agen-AI-Inaproc
```

### 3. Setup Virtual Environment
```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Konfigurasi

### Setup File .env

1. Copy file contoh:
```bash
cp .env.example .env
```

2. Edit file `.env`:
```env
# API Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
API_PORT=8000
DEBUG=True

# Database (Optional)
DATABASE_URL=postgresql://user:password@localhost:5432/inaproc_db

# Agent Configuration
AGENT_MODEL=gpt-4
AGENT_TEMPERATURE=0.7
MAX_TOKENS=2000

# Logging
LOG_LEVEL=INFO
```

### Penjelasan Konfigurasi:
- **OPENAI_API_KEY**: Key dari OpenAI (https://platform.openai.com/api-keys)
- **API_PORT**: Port untuk menjalankan API (default: 8000)
- **DEBUG**: Mode debug (True untuk development, False untuk production)
- **AGENT_MODEL**: Model OpenAI yang digunakan (gpt-4, gpt-3.5-turbo, dll)
- **AGENT_TEMPERATURE**: Kreativitas AI (0.0-1.0, 0 = deterministic, 1 = creative)
- **MAX_TOKENS**: Maksimal token dalam response

---

## Menjalankan Aplikasi

### Option 1: Menjalankan Langsung (Development)

```bash
# Pastikan virtual environment sudah aktif
python main.py
```

Output yang diharapkan:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

Buka browser: http://localhost:8000

### Option 2: Menggunakan Docker

```bash
# Build image
docker build -t agen-ai-inaproc .

# Run container
docker run -p 8000:8000 --env-file .env agen-ai-inaproc
```

### Option 3: Menggunakan Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

---

## Menggunakan API

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "agent"
}
```

### 2. Chat dengan Agent

**Endpoint**: `POST /api/agent/chat`

```bash
curl -X POST http://localhost:8000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Halo, siapa nama Anda?",
    "context": {
      "user_id": "user123",
      "session": "session456"
    }
  }'
```

Response:
```json
{
  "message": "Halo! Saya adalah Agen AI Inaproc, asisten profesional Anda. Bagaimana saya bisa membantu Anda hari ini?",
  "timestamp": "2026-05-24T14:00:00"
}
```

### 3. Execute Task

**Endpoint**: `POST /api/agent/task`

```bash
curl -X POST http://localhost:8000/api/agent/task \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Buatkan saya ringkasan tentang machine learning dalam 3 poin",
    "task_type": "analysis",
    "metadata": {
      "priority": "high",
      "deadline": "2026-05-25"
    }
  }'
```

Response:
```json
{
  "status": "success",
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "result": "1. Machine Learning adalah cabang AI yang memungkinkan sistem belajar dari data...",
  "error": null,
  "timestamp": "2026-05-24T14:05:00"
}
```

---

## Contoh Penggunaan

### Python Client

```python
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

# 1. Health Check
response = requests.get(f"{BASE_URL}/health")
print("Health:", response.json())

# 2. Chat dengan Agent
chat_data = {
    "message": "Apa itu artificial intelligence?",
    "context": {"topic": "education"}
}
response = requests.post(
    f"{BASE_URL}/api/agent/chat",
    headers=HEADERS,
    json=chat_data
)
print("Chat Response:", response.json())

# 3. Execute Task
task_data = {
    "prompt": "Jelaskan konsep neural network dengan bahasa sederhana",
    "task_type": "education",
    "metadata": {"language": "id"}
}
response = requests.post(
    f"{BASE_URL}/api/agent/task",
    headers=HEADERS,
    json=task_data
)
result = response.json()
print(f"Task ID: {result['task_id']}")
print(f"Result: {result['result']}")
```

### JavaScript/Node.js Client

```javascript
const axios = require('axios');

const BASE_URL = "http://localhost:8000";

// 1. Health Check
async function healthCheck() {
  try {
    const response = await axios.get(`${BASE_URL}/health`);
    console.log("Health:", response.data);
  } catch (error) {
    console.error("Error:", error.message);
  }
}

// 2. Chat
async function chatWithAgent(message) {
  try {
    const response = await axios.post(
      `${BASE_URL}/api/agent/chat`,
      {
        message: message,
        context: { user_id: "user123" }
      }
    );
    console.log("Response:", response.data.message);
  } catch (error) {
    console.error("Error:", error.message);
  }
}

// 3. Execute Task
async function executeTask(prompt) {
  try {
    const response = await axios.post(
      `${BASE_URL}/api/agent/task`,
      {
        prompt: prompt,
        task_type: "general"
      }
    );
    console.log("Task Result:", response.data.result);
  } catch (error) {
    console.error("Error:", error.message);
  }
}

// Run
healthCheck();
chatWithAgent("Halo, bagaimana kabar Anda?");
executeTask("Buatkan program hello world dalam Python");
```

### cURL Examples

```bash
# Contoh 1: Simple Chat
curl -X POST http://localhost:8000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Berapa hasil dari 5 + 3?"}'

# Contoh 2: Task dengan Metadata
curl -X POST http://localhost:8000/api/agent/task \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Buatkan kode Python untuk membaca file CSV",
    "task_type": "coding",
    "metadata": {"language": "python", "complexity": "beginner"}
  }'

# Contoh 3: Chat dengan Context
curl -X POST http://localhost:8000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Lanjutkan diskusi kita sebelumnya",
    "context": {
      "user_id": "user_001",
      "session_id": "sess_001",
      "previous_topic": "machine learning"
    }
  }'
```

---

## Advanced Usage

### 1. Custom Agent Configuration

Edit `src/agent/agent.py`:

```python
class InaprocAgent:
    def __init__(self):
        self.llm = OpenAI(
            openai_api_key=config.OPENAI_API_KEY,
            model_name="gpt-4",  # Ubah model
            temperature=0.5,      # Ubah kreativitas
            max_tokens=4000       # Ubah max tokens
        )
```

### 2. Menambah Endpoint Custom

Edit `src/api/routes.py`:

```python
@router.post("/api/agent/custom")
async def custom_endpoint(request: dict):
    """Endpoint custom Anda"""
    # Logic Anda di sini
    return {"result": "custom response"}
```

### 3. Integration dengan Database

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = config.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## Troubleshooting

### Problem 1: `ModuleNotFoundError: No module named 'fastapi'`

**Solusi:**
```bash
# Pastikan virtual environment aktif
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# Install ulang requirements
pip install -r requirements.txt
```

### Problem 2: `openai.error.AuthenticationError`

**Penyebab:** OpenAI API key salah atau tidak ada

**Solusi:**
1. Pastikan Anda punya OpenAI API key dari https://platform.openai.com/api-keys
2. Periksa file `.env`:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

### Problem 3: Port 8000 sudah terpakai

**Solusi:**
```bash
# Gunakan port lain di .env
API_PORT=8001

# Atau kill process yang menggunakan port 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Problem 4: Database connection error

**Solusi:**
```bash
# Pastikan PostgreSQL berjalan
# Atau gunakan docker-compose
docker-compose up -d postgres
```

### Problem 5: Timeout atau response lambat

**Penyebab:** Model AI atau network lambat

**Solusi:**
1. Naikkan timeout di client
2. Gunakan model lebih cepat (gpt-3.5-turbo daripada gpt-4)
3. Kurangi MAX_TOKENS di `.env`

---

## Tips & Best Practices

✅ **DO:**
- Gunakan environment variables untuk sensitif data
- Set DEBUG=False di production
- Monitor API logs untuk issues
- Gunakan appropriate TEMPERATURE untuk use case
- Implement rate limiting

❌ **DON'T:**
- Commit `.env` file ke repository
- Hardcode API keys
- Gunakan gpt-4 untuk semua (biaya tinggi)
- Biarkan DEBUG=True di production
- Ignore error messages

---

## Support & Resources

- 📚 OpenAI Documentation: https://platform.openai.com/docs
- 🚀 FastAPI Docs: https://fastapi.tiangolo.com
- 🔗 LangChain Docs: https://python.langchain.com
- 💬 Issues: https://github.com/agnijayamandiri2026-cmd/Agen-AI-Inaproc/issues

---

**Selamat menggunakan Agen AI Inaproc! 🚀**

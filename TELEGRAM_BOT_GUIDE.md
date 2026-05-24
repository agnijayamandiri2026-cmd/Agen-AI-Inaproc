# Panduan Instalasi Bot Telegram - Agen AI Inaproc

## 📱 Instalasi Bot Telegram

### Langkah 1: Buat Bot di BotFather

1. Buka Telegram dan cari **@BotFather**
2. Kirim perintah: `/start`
3. Kirim: `/newbot`
4. Ikuti instruksi:
   - Nama Bot: `Agen AI Inaproc Bot` (atau nama pilihan Anda)
   - Username Bot: `inaproc_agent_bot` (harus unik, akhiri dengan "bot")

5. **Copy token yang diberikan** - ini adalah `TELEGRAM_BOT_TOKEN`

Contoh token: `6234567890:ABCDEfghijklmNOpQRstUvwxyz1234567890`

---

### Langkah 2: Setup Environment Variables

Update file `.env`:

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_WEBHOOK_URL=https://your-domain.com
TELEGRAM_WEBHOOK_PATH=/telegram/webhook
```

---

### Langkah 3: Mode Operasi Bot

#### **Option A: Polling Mode (Lokal/Testing)**

Polling mode cocok untuk development dan testing lokal.

```bash
# Terminal 1: Jalankan API Server
python main.py

# Terminal 2: Jalankan Telegram Bot
python telegram_bot.py
```

✅ Bot akan langsung aktif dan merespons pesan
✅ Tidak perlu domain/HTTPS
✅ Cocok untuk testing

❌ Polling lebih boros resource
❌ Kurang scalable untuk production

---

#### **Option B: Webhook Mode (Production)**

Webhook mode cocok untuk production dengan domain HTTPS.

```bash
# 1. Setup domain dan HTTPS
# Pastikan Anda punya domain dengan sertifikat SSL/TLS

# 2. Update .env
TELEGRAM_WEBHOOK_URL=https://your-domain.com
TELEGRAM_WEBHOOK_PATH=/telegram/webhook

# 3. Jalankan API
python main.py
```

Webhook akan otomatis mendaftar ke Telegram.

✅ Event-driven (lebih efisien)
✅ Scalable untuk banyak pengguna
✅ Lebih cepat

❌ Perlu domain HTTPS
❌ Setup lebih kompleks

---

## 🚀 Quick Start - Polling Mode

### 1. Setup

```bash
# Clone repo
git clone https://github.com/agnijayamandiri2026-cmd/Agen-AI-Inaproc.git
cd Agen-AI-Inaproc

# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Konfigurasi

```bash
cp .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=sk-your-openai-key
TELEGRAM_BOT_TOKEN=123456:ABCDEFgh-ijklmnop_qrstuvwxyz
DEBUG=True
```

### 3. Jalankan Bot

**Terminal 1: API Server**
```bash
python main.py
```

Output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2: Bot Telegram**
```bash
python telegram_bot.py
```

Output:
```
INFO:     root - Starting Telegram Bot...
INFO:     src.telegram.bot - Telegram bot started (polling mode)
```

### 4. Test Bot

Buka Telegram dan cari username bot Anda, lalu:

```
/start
Halo, bagaimana kabar Anda?
/help
/about
Buatkan kode Python hello world
```

---

## 📦 Docker Deployment

### Single Container (Bot + API)

```bash
# Build
docker build -t agen-ai-telegram .

# Run
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-xxx \
  -e TELEGRAM_BOT_TOKEN=123:ABC \
  agen-ai-telegram python telegram_bot.py
```

### Docker Compose (Recommended)

```yaml
# docker-compose.yml
version: '3.8'

services:
  telegram-bot:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - DATABASE_URL=postgresql://inaproc:password@postgres:5432/inaproc_db
      - DEBUG=False
    depends_on:
      - postgres
    command: python telegram_bot.py

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - DATABASE_URL=postgresql://inaproc:password@postgres:5432/inaproc_db
      - DEBUG=False
    depends_on:
      - postgres
    command: python main.py

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: inaproc
      POSTGRES_PASSWORD: password
      POSTGRES_DB: inaproc_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Jalankan:
```bash
docker-compose up -d
```

---

## 💬 Fitur Bot Telegram

### Perintah Tersedia

| Perintah | Fungsi |
|----------|--------|
| `/start` | Mulai bot |
| `/help` | Lihat bantuan |
| `/about` | Info tentang bot |
| `/clear` | Hapus history |

### Kemampuan

✅ **Chat** - Tanya apa saja ke AI
```
User: "Apa itu machine learning?"
Bot: "Machine learning adalah..."
```

✅ **Coding** - Minta bantuan kode
```
User: "Buatkan kode Python untuk membaca file CSV"
Bot: "import pandas as pd..."
```

✅ **Analysis** - Analisis dan penjelasan
```
User: "Jelaskan REST API"
Bot: "REST API adalah arsitektur..."
```

✅ **Creative** - Brainstorming dan writing
```
User: "Buatkan cerita pendek"
Bot: "Hari itu dimulai dengan..."
```

---

## 🔧 Konfigurasi Lanjutan

### Mengubah Parameter AI

Edit `src/telegram/bot.py` atau `.env`:

```env
# Model lebih cepat (lebih murah)
AGENT_MODEL=gpt-3.5-turbo

# Model lebih powerful
AGENT_MODEL=gpt-4

# Kreativitas (0.0 = deterministic, 1.0 = creative)
AGENT_TEMPERATURE=0.7

# Max tokens output
MAX_TOKENS=2000
```

### Custom Responses

Edit `src/telegram/bot.py` - ubah text di method `start()`, `help_command()`, dll.

### Database Integration

Uncomment dan setup di `src/telegram/bot.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Track user conversations
async def save_message(user_id, message, response):
    # Save ke database
    pass
```

---

## 🐛 Troubleshooting

### Problem 1: "Invalid token"

**Solusi:**
- Verifikasi token dari BotFather
- Pastikan tidak ada space di `.env`
- Restart bot setelah ubah token

```bash
# Validate token
curl -s -X GET https://api.telegram.org/bot<YOUR_TOKEN>/getMe | python -m json.tool
```

### Problem 2: Bot tidak merespons

**Penyebab & Solusi:**

```bash
# 1. Pastikan OPENAI_API_KEY benar
# 2. Check logs untuk error
python telegram_bot.py  # Lihat output

# 3. Pastikan dependencies ter-install
pip install -r requirements.txt

# 4. Restart bot
Ctrl+C
python telegram_bot.py
```

### Problem 3: Timeout atau respons lambat

```env
# Gunakan model lebih cepat
AGENT_MODEL=gpt-3.5-turbo

# Kurangi MAX_TOKENS
MAX_TOKENS=1000

# Naikkan TEMPERATURE untuk variasi
AGENT_TEMPERATURE=0.5
```

### Problem 4: Memory/CPU tinggi

Gunakan webhook mode daripada polling:

```bash
# Setup webhook di config
# Deploy ke server dengan HTTPS
```

---

## 📊 Monitoring

### View Logs

```bash
# Streaming logs (polling)
tail -f logs/telegram.log

# Docker logs
docker-compose logs -f telegram-bot
```

### Health Check

```bash
# API Health
curl http://localhost:8000/health

# Telegram Status
curl http://localhost:8000/telegram/status
```

---

## 🚀 Deployment ke Production

### Deploy ke Heroku

```bash
# 1. Login heroku
heroku login

# 2. Create app
heroku create agen-ai-inaproc

# 3. Set environment
heroku config:set OPENAI_API_KEY=sk-xxx
heroku config:set TELEGRAM_BOT_TOKEN=123:ABC

# 4. Deploy
git push heroku main
```

### Deploy ke VPS (Ubuntu/Debian)

```bash
# 1. SSH ke server
ssh user@server.com

# 2. Clone repo
git clone https://github.com/agnijayamandiri2026-cmd/Agen-AI-Inaproc.git
cd Agen-AI-Inaproc

# 3. Setup systemd service
sudo nano /etc/systemd/system/agen-telegram.service
```

Isi file:
```ini
[Unit]
Description=Agen AI Inaproc Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Agen-AI-Inaproc
ExecStart=/home/ubuntu/Agen-AI-Inaproc/venv/bin/python telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Jalankan:
```bash
sudo systemctl daemon-reload
sudo systemctl start agen-telegram
sudo systemctl enable agen-telegram

# Check status
sudo systemctl status agen-telegram
```

---

## 📚 Resources

- 📖 [Python Telegram Bot Docs](https://docs.python-telegram-bot.org/)
- 🤖 [OpenAI API](https://platform.openai.com/docs)
- 📱 [Telegram Bot API](https://core.telegram.org/bots/api)
- 🐳 [Docker Guide](https://docs.docker.com/)

---

**Bot Telegram Agen AI Inaproc siap digunakan! 🚀**

"""
Telegram Bot - Agen AI Inaproc
Bot yang terintegrasi dengan FastAPI untuk memberikan response AI

Jalankan dengan: python telegram_bot.py
"""

import os
import logging
import httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramBot:
    """Telegram Bot Handler untuk Agen AI Inaproc"""
    
    def __init__(self):
        """Initialize bot dengan token dari .env"""
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.api_url = os.getenv("API_URL", "http://localhost:8000")
        
        if not self.token:
            logger.error("❌ TELEGRAM_BOT_TOKEN tidak ditemukan di .env")
            raise ValueError("Missing TELEGRAM_BOT_TOKEN in .env")
        
        logger.info(f"✅ Bot Token: {self.token[:30]}...")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /start command
        Menampilkan welcome message
        """
        try:
            user = update.effective_user
            
            welcome_text = f"""
👋 Halo {user.first_name}!

Saya adalah **Agen AI Inaproc**, asisten AI profesional Anda.

**📋 Perintah Tersedia:**
• `/start` - Mulai / Reset
• `/help` - Lihat bantuan
• `/about` - Tentang bot
• `/clear` - Hapus history chat
• `/status` - Cek status bot

**💬 Cara Menggunakan:**
Cukup ketik pesan apapun dan saya akan membalas dengan respons AI yang relevan.

**Contoh:**
- "Halo, apa kabar?"
- "Buatkan kode Python untuk hello world"
- "Jelaskan machine learning"

Silakan mulai dengan mengetik pesan! 🚀
            """
            
            await update.message.reply_text(welcome_text, parse_mode="Markdown")
            logger.info(f"✅ /start - User {user.id} ({user.username}) started bot")
            
        except Exception as e:
            logger.error(f"❌ Error in start: {str(e)}")
            await update.message.reply_text("❌ Terjadi kesalahan saat start bot")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /help command
        Menampilkan bantuan lengkap
        """
        try:
            help_text = """
📚 **BANTUAN - Agen AI Inaproc Bot**

**Perintah Bot:**
• `/start` - Mulai ulang bot
• `/help` - Bantuan ini
• `/about` - Informasi bot
• `/clear` - Hapus history chat
• `/status` - Status bot dan API

**Cara Chat:**
1. Ketik pesan apapun
2. Bot akan memproses dengan AI
3. Tunggu response

**Contoh Pertanyaan:**
✓ "Apa itu machine learning?"
✓ "Buatkan function Python untuk..."
✓ "Jelaskan tentang..."
✓ "Bantu saya dengan..."

**Catatan:**
• Bot menggunakan AI untuk memberikan jawaban
• Pastikan API server sedang berjalan
• Response tergantung pada API key yang dikonfigurasi

**Troubleshooting:**
Jika bot tidak merespons:
1. Kirim `/status` untuk cek status
2. Tunggu beberapa detik
3. Coba pesan lagi

Butuh bantuan lebih? Hubungi admin.
            """
            
            await update.message.reply_text(help_text, parse_mode="Markdown")
            logger.info(f"✅ /help - User {update.effective_user.id} requested help")
            
        except Exception as e:
            logger.error(f"❌ Error in help: {str(e)}")
            await update.message.reply_text("❌ Terjadi kesalahan")
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /about command
        Menampilkan informasi bot
        """
        try:
            about_text = """
ℹ️ **TENTANG - Agen AI Inaproc**

**Bot Info:**
• Nama: Agen AI Inaproc Bot
• Versi: 1.0.0
• Type: AI Assistant Telegram Bot

**Fitur:**
✓ Chat dengan AI
✓ Response generation
✓ Multi-language support
✓ History management
✓ Real-time processing

**Teknologi:**
• Python 3.9+
• python-telegram-bot
• FastAPI
• OpenAI API
• AsyncIO

**Developer:**
Agen AI Inaproc Team

**Repository:**
https://github.com/agnijayamandiri2026-cmd/Agen-AI-Inaproc

**Support:**
Hubungi admin untuk bantuan lebih lanjut.
            """
            
            await update.message.reply_text(about_text, parse_mode="Markdown")
            logger.info(f"✅ /about - User {update.effective_user.id} requested info")
            
        except Exception as e:
            logger.error(f"❌ Error in about: {str(e)}")
            await update.message.reply_text("❌ Terjadi kesalahan")
    
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /clear command
        Hapus conversation history
        """
        try:
            user = update.effective_user
            context.user_data.clear()
            
            clear_text = """
✅ **History Cleared**

Chat history Anda telah dihapus.
Dimulai fresh conversation! 🔄
            """
            
            await update.message.reply_text(clear_text, parse_mode="Markdown")
            logger.info(f"✅ /clear - User {user.id} cleared history")
            
        except Exception as e:
            logger.error(f"❌ Error in clear: {str(e)}")
            await update.message.reply_text("❌ Terjadi kesalahan")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /status command
        Cek status bot dan API
        """
        try:
            status_text = "🔍 **Mengecek Status...**\n"
            
            # Check API status
            try:
                async with httpx.AsyncClient(timeout=5) as client:
                    response = await client.get(f"{self.api_url}/health")
                    if response.status_code == 200:
                        status_text += "✅ API Server: **ONLINE**\n"
                    else:
                        status_text += "❌ API Server: **OFFLINE**\n"
            except Exception as e:
                status_text += f"❌ API Server: **OFFLINE** ({type(e).__name__})\n"
            
            # Bot status
            status_text += "✅ Bot Status: **ONLINE**\n"
            status_text += "✅ Polling: **ACTIVE**\n"
            
            # User info
            user = update.effective_user
            status_text += f"\n👤 **User Info:**\n"
            status_text += f"• ID: `{user.id}`\n"
            status_text += f"• Username: `@{user.username}`\n"
            status_text += f"• Name: `{user.first_name}`\n"
            
            await update.message.reply_text(status_text, parse_mode="Markdown")
            logger.info(f"✅ /status - User {user.id} checked status")
            
        except Exception as e:
            logger.error(f"❌ Error in status: {str(e)}")
            await update.message.reply_text("❌ Terjadi kesalahan saat check status")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle regular messages
        Proses pesan user dan kirim ke API
        """
        try:
            user = update.effective_user
            message_text = update.message.text
            
            logger.info(f"📨 Pesan dari {user.id} (@{user.username}): {message_text}")
            
            # Show typing indicator
            await update.effective_chat.send_action("typing")
            
            # Try to get response from API
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    # Call API endpoint
                    response = await client.post(
                        f"{self.api_url}/api/agent/chat",
                        json={"prompt": message_text, "user_id": str(user.id)},
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        ai_response = data.get("response", "Maaf, tidak ada response dari AI")
                        logger.info(f"✅ API Response received")
                    else:
                        ai_response = f"⚠️ API Error (Status {response.status_code})\n\nSilakan coba lagi nanti atau hubungi admin."
                        logger.error(f"❌ API Error: {response.status_code}")
            
            except httpx.TimeoutException:
                ai_response = "⏱️ **Timeout**\n\nAPI server tidak merespons dalam waktu yang ditentukan.\n\nCoba lagi atau hubungi admin."
                logger.error("❌ API Timeout")
            
            except httpx.ConnectError:
                ai_response = "❌ **Connection Error**\n\nTidak bisa terhubung ke API server.\n\nPastikan API server sedang berjalan di http://localhost:8000"
                logger.error("❌ API Connection Error")
            
            except Exception as e:
                ai_response = f"❌ **Error**\n\nTerjadi kesalahan: {str(e)}\n\nPastikan API server sedang berjalan."
                logger.error(f"❌ API Error: {str(e)}")
            
            # Send response
            if len(ai_response) > 4096:
                # Split message if too long
                for i in range(0, len(ai_response), 4096):
                    await update.message.reply_text(ai_response[i:i+4096], parse_mode="Markdown")
            else:
                await update.message.reply_text(ai_response, parse_mode="Markdown")
            
            logger.info(f"✅ Response sent to {user.id}")
            
        except Exception as e:
            logger.error(f"❌ Error handling message: {str(e)}")
            await update.message.reply_text(f"❌ Terjadi kesalahan: {str(e)}")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle errors
        Log semua error yang terjadi
        """
        logger.error(f"❌ Update caused error: {context.error}")
    
    async def run(self):
        """
        Run bot
        Setup handlers dan mulai polling
        """
        logger.info("🤖 Membuat Telegram Bot Application...")
        
        # Create application
        app = Application.builder().token(self.token).build()
        
        logger.info("📋 Menambahkan handlers...")
        
        # Add command handlers
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("about", self.about_command))
        app.add_handler(CommandHandler("clear", self.clear_command))
        app.add_handler(CommandHandler("status", self.status_command))
        
        # Add message handler (untuk pesan biasa)
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Add error handler
        app.add_error_handler(self.error_handler)
        
        logger.info("✅ Handler berhasil ditambahkan")
        logger.info("🚀 Bot sedang start dengan polling mode...")
        
        # Start bot
        await app.start()
        logger.info("✅ Bot Application started!")
        
        # Start polling
        logger.info("📡 Bot mulai listen ke messages...")
        await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        logger.info("✅ Bot Polling started!")
        
        # Display ready message
        logger.info("════════════════════════════════════")
        logger.info("🎉 BOT READY!")
        logger.info("📱 Buka Telegram dan cari bot Anda")
        logger.info("💬 Kirim /start atau pesan apapun")
        logger.info("════════════════════════════════════")
        
        # Keep bot running indefinitely
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("⏹️ Stopping bot...")
            await app.updater.stop()
            await app.stop()

async def main():
    """
    Main entry point
    """
    try:
        logger.info("🚀 Starting Agen AI Inaproc Telegram Bot...")
        logger.info(f"📝 API URL: {os.getenv('API_URL', 'http://localhost:8000')}")
        
        bot = TelegramBot()
        await bot.run()
        
    except KeyboardInterrupt:
        logger.info("❌ Bot stopped by user (Ctrl+C)")
    
    except ValueError as e:
        logger.error(f"❌ Configuration Error: {str(e)}")
        logger.error("📝 Pastikan TELEGRAM_BOT_TOKEN sudah diset di file .env")
    
    except Exception as e:
        logger.error(f"❌ Fatal Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

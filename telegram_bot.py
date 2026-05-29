"""
Telegram Bot - Agen AI Inaproc
Bot yang terintegrasi dengan FastAPI untuk memberikan response AI

Jalankan dengan: python telegram_bot.py
"""

import os
import sys
import logging
import httpx
import asyncio
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
        self.application = None
        self.running = False
        
        if not self.token:
            logger.error("❌ TELEGRAM_BOT_TOKEN tidak ditemukan di .env")
            logger.error("📝 Pastikan TELEGRAM_BOT_TOKEN sudah diset di file .env")
            raise ValueError("Missing TELEGRAM_BOT_TOKEN in .env")
        
        logger.info(f"✅ Bot Token: {self.token[:30]}...")
        logger.info(f"📝 API URL: {self.api_url}")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
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
Cukup ketik pesan apapun dan saya akan membalas dengan respons.

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
            try:
                await update.message.reply_text("❌ Terjadi kesalahan saat start bot")
            except:
                pass
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
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
2. Bot akan memproses
3. Tunggu response

**Contoh Pertanyaan:**
✓ "Apa itu machine learning?"
✓ "Buatkan function Python"
✓ "Jelaskan tentang..."
✓ "Bantu saya dengan..."

**Catatan:**
• Bot menggunakan API untuk memberikan jawaban
• Pastikan API server sedang berjalan
• Response tergantung konfigurasi

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
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /about command"""
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
    
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /clear command"""
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
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        try:
            status_text = "🔍 **Mengecek Status...**\n\n"
            
            # Check API status
            api_online = False
            try:
                async with httpx.AsyncClient(timeout=5) as client:
                    response = await client.get(f"{self.api_url}/health")
                    if response.status_code == 200:
                        status_text += "✅ API Server: **ONLINE**\n"
                        api_online = True
                    else:
                        status_text += f"❌ API Server: **OFFLINE** (Status {response.status_code})\n"
            except httpx.ConnectError:
                status_text += f"❌ API Server: **OFFLINE** (Connection failed)\n"
                logger.warning(f"⚠️ Cannot connect to API at {self.api_url}")
            except httpx.TimeoutException:
                status_text += "❌ API Server: **TIMEOUT**\n"
            except Exception as e:
                status_text += f"❌ API Server: **ERROR** ({type(e).__name__})\n"
            
            # Bot status
            status_text += "✅ Bot Status: **ONLINE**\n"
            status_text += "✅ Polling: **ACTIVE**\n"
            
            # User info
            user = update.effective_user
            status_text += f"\n👤 **User Info:**\n"
            status_text += f"• ID: `{user.id}`\n"
            status_text += f"• Username: `@{user.username or 'N/A'}`\n"
            status_text += f"• Name: `{user.first_name}`\n"
            
            if not api_online:
                status_text += "\n⚠️ **API Offline!**\n"
                status_text += "Pastikan API server sedang berjalan di terminal lain dengan: `python main.py`"
            
            await update.message.reply_text(status_text, parse_mode="Markdown")
            logger.info(f"✅ /status - User {user.id} checked status")
            
        except Exception as e:
            logger.error(f"❌ Error in status: {str(e)}")
            try:
                await update.message.reply_text(f"❌ Error checking status: {str(e)}")
            except:
                pass
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        try:
            user = update.effective_user
            message_text = update.message.text
            
            logger.info(f"📨 Pesan dari {user.id} (@{user.username}): {message_text[:50]}...")
            
            # Show typing indicator
            await update.effective_chat.send_action("typing")
            
            # Try to get response from API
            ai_response = None
            
            try:
                async with httpx.AsyncClient(timeout=15) as client:
                    logger.info(f"📡 Mengirim request ke {self.api_url}/api/agent/chat")
                    
                    response = await client.post(
                        f"{self.api_url}/api/agent/chat",
                        json={
                            "prompt": message_text,
                            "user_id": str(user.id)
                        },
                        headers={"Content-Type": "application/json"}
                    )
                    
                    logger.info(f"📥 API Response Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        ai_response = data.get("response", "Maaf, tidak ada response dari API")
                        logger.info(f"✅ API Response received successfully")
                    else:
                        ai_response = f"⚠️ **API Error** (Status {response.status_code})\n\nSilakan coba lagi nanti atau hubungi admin."
                        logger.error(f"❌ API Error Status: {response.status_code}")
                        logger.error(f"Response body: {response.text}")
            
            except httpx.ConnectError as e:
                ai_response = f"❌ **Connection Error**\n\nTidak bisa terhubung ke API server di {self.api_url}\n\n✅ **Solusi:**\nPastikan API server sedang berjalan dengan command:\n```\npython main.py\n```"
                logger.error(f"❌ API Connection Error: {str(e)}")
            
            except httpx.TimeoutException:
                ai_response = "⏱️ **Timeout**\n\nAPI server tidak merespons dalam waktu yang ditentukan.\n\nCoba lagi atau hubungi admin."
                logger.error("❌ API Timeout")
            
            except Exception as e:
                ai_response = f"❌ **Error**\n\nTerjadi kesalahan saat menghubungi API:\n`{str(e)}`\n\nPastikan API server sedang berjalan."
                logger.error(f"❌ API Error: {str(e)}")
            
            # Send response
            if ai_response:
                if len(ai_response) > 4096:
                    # Split message if too long
                    for i in range(0, len(ai_response), 4096):
                        await update.message.reply_text(
                            ai_response[i:i+4096],
                            parse_mode="Markdown"
                        )
                else:
                    await update.message.reply_text(ai_response, parse_mode="Markdown")
                
                logger.info(f"✅ Response sent to user {user.id}")
            
        except Exception as e:
            logger.error(f"❌ Error handling message: {str(e)}")
            try:
                await update.message.reply_text(f"❌ Terjadi kesalahan: {str(e)}")
            except:
                pass
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"❌ Update caused error: {context.error}")
    
    async def run(self):
        """Run bot dengan proper initialization"""
        try:
            logger.info("🤖 Membuat Telegram Bot Application...")
            
            # Create application
            self.application = Application.builder().token(self.token).build()
            
            logger.info("📋 Menambahkan command handlers...")
            
            # Add command handlers
            self.application.add_handler(CommandHandler("start", self.start))
            self.application.add_handler(CommandHandler("help", self.help_command))
            self.application.add_handler(CommandHandler("about", self.about_command))
            self.application.add_handler(CommandHandler("clear", self.clear_command))
            self.application.add_handler(CommandHandler("status", self.status_command))
            
            logger.info("📋 Menambahkan message handler...")
            
            # Add message handler (untuk pesan biasa)
            self.application.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
            )
            
            logger.info("📋 Menambahkan error handler...")
            
            # Add error handler
            self.application.add_error_handler(self.error_handler)
            
            logger.info("✅ Semua handler berhasil ditambahkan")
            logger.info("🚀 Bot sedang start dengan polling mode...")
            
            # Initialize application
            logger.info("⚙️ Initializing bot application...")
            await self.application.initialize()
            logger.info("✅ Bot application initialized!")
            
            # Start application
            logger.info("🔌 Starting bot application...")
            await self.application.start()
            logger.info("✅ Bot application started!")
            
            # Start polling
            logger.info("📡 Bot mulai listen ke messages...")
            await self.application.updater.start_polling(
                allowed_updates=Update.ALL_TYPES,
                timeout=30,
                read_timeout=10
            )
            logger.info("✅ Bot polling started!")
            
            # Display ready message
            logger.info("════════════════════════════════════")
            logger.info("🎉 BOT READY!")
            logger.info("📱 Buka Telegram dan cari bot Anda")
            logger.info("💬 Kirim /start atau pesan apapun")
            logger.info("════════════════════════════════════")
            
            self.running = True
            
            # Keep bot running indefinitely
            try:
                while self.running:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("⏹️ Keyboard interrupt received, stopping bot...")
        
        finally:
            # Graceful shutdown
            logger.info("🛑 Shutting down bot...")
            try:
                if self.application:
                    await self.application.updater.stop()
                    logger.info("✅ Updater stopped")
                    
                    await self.application.stop()
                    logger.info("✅ Application stopped")
                    
                    await self.application.shutdown()
                    logger.info("✅ Application shutdown")
            except Exception as e:
                logger.error(f"❌ Error during shutdown: {str(e)}")
            
            logger.info("✅ Bot stopped successfully")
            self.running = False

async def main():
    """Main entry point"""
    try:
        logger.info("════════════════════════════════════")
        logger.info("🚀 Starting Agen AI Inaproc Telegram Bot...")
        logger.info(f"📝 API URL: {os.getenv('API_URL', 'http://localhost:8000')}")
        logger.info("════════════════════════════════════")
        
        bot = TelegramBot()
        await bot.run()
        
    except KeyboardInterrupt:
        logger.info("❌ Bot stopped by user (Ctrl+C)")
    
    except ValueError as e:
        logger.error(f"❌ Configuration Error: {str(e)}")
        logger.error("📝 Pastikan TELEGRAM_BOT_TOKEN sudah diset di file .env")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"❌ Fatal Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot terminated by user")
        sys.exit(0)

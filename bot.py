"""
Telegram Social Media Video Downloader Bot
Main application file handling Telegram bot interactions with interactive buttons.
"""

import os
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

from url_handler import URLHandler
from video_downloader import VideoDownloader


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramBot:
    """Main bot class handling message processing and responses."""
    
    def __init__(self):
        """Initialize the bot with configuration."""
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
        
        self.download_dir = os.getenv('DOWNLOAD_DIR', './downloads')
        self.web_server_url = os.getenv('WEB_SERVER_URL', '')
        
        self.downloader = VideoDownloader(self.download_dir)
        self.url_handler = URLHandler()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = (
            "🎥 *Telegram Social Media Video Downloader Bot*\\n\\n"
            "Send me links from:\\n"
            "• YouTube\\n"
            "• Facebook\\n"
            "• X (Twitter)\\n"
            "• Instagram\\n"
            "• TikTok\\n\\n"
            "*Usage:*\\n"
            "Just send a link - I'll download it and show you buttons to choose:\\n"
            "• 📥 Get Link - Receive download link\\n"
            "• 📹 Send Video - Get video in chat\\n\\n"
            "You can send multiple links at once!"
        )
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_message = (
            "*How to use:*\\n\\n"
            "1. Send me a video URL from supported platforms\\n"
            "2. Wait for download to complete\\n"
            "3. Click a button to choose how to receive it\\n\\n"
            "*Examples:*\\n"
            "`https://youtube.com/watch?v=abc123`\\n"
            "`https://tiktok.com/@user/video/123`\\n"
            "`https://instagram.com/p/abc`"
        )
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def process_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process incoming messages containing video URLs."""
        message_text = update.message.text
        logger.info(f"Processing message: {message_text[:100]}...")
        
        # Extract URLs from message
        urls = self.url_handler.extract_urls(message_text)
        
        if not urls:
            await update.message.reply_text(
                "❌ No valid URLs found. Please send a link from YouTube, Facebook, X, Instagram, or TikTok."
            )
            return
        
        # Send processing notification
        processing_msg = await update.message.reply_text(
            f"⏳ Processing {len(urls)} link(s)..."
        )
        
        # Process each URL
        for url_info in urls:
            url = url_info['url']
            platform = url_info['platform']
            
            logger.info(f"Processing {platform} URL: {url}")
            
            # Download video
            download_result = self.downloader.download_video(url, platform)
            
            # Check if download succeeded
            if not download_result['success']:
                logger.warning(f"Download failed for {url}: {download_result['error']}")
                await update.message.reply_text(f"❌ Download failed: {download_result['error']}")
                continue
            
            # Store file info for callback
            file_path = download_result['file_path']
            filename = Path(file_path).name
            title = download_result.get('title', 'Video')
            
            # Generate download link
            if self.web_server_url:
                download_link = f"{self.web_server_url.rstrip('/')}/{filename}"
            else:
                download_link = f"file:///{file_path}"
            
            # Create unique identifier for this download
            video_id = filename.replace('.', '_').replace('-', '_')
            
            # Store in context for callback handler
            if 'downloads' not in context.bot_data:
                context.bot_data['downloads'] = {}
            
            context.bot_data['downloads'][video_id] = {
                'file_path': file_path,
                'download_link': download_link,
                'title': title,
                'url': url
            }
            
            # Create inline keyboard with two options
            keyboard = [
                [
                    InlineKeyboardButton("📥 Get Link", callback_data=f"link_{video_id}"),
                    InlineKeyboardButton("📹 Send Video", callback_data=f"file_{video_id}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send message with buttons
            await update.message.reply_text(
                f"✅ Downloaded: {title}\\n\\nChoose how to receive:",
                reply_markup=reply_markup
            )
        
        # Delete processing message
        await processing_msg.delete()
        
        logger.info(f"Completed processing {len(urls)} URLs")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button clicks."""
        query = update.callback_query
        await query.answer()  # Acknowledge the button click
        
        # Parse callback data
        try:
            action, video_id = query.data.split('_', 1)
        except ValueError:
            await query.edit_message_text("❌ Error: Invalid button data.")
            return
        
        # Retrieve stored data
        if 'downloads' not in context.bot_data or video_id not in context.bot_data['downloads']:
            await query.edit_message_text("❌ Error: Video data expired. Please download again.")
            return
        
        video_data = context.bot_data['downloads'][video_id]
        file_path = video_data['file_path']
        download_link = video_data['download_link']
        title = video_data['title']
        
        if action == 'link':
            # User wants the download link
            await query.edit_message_text(
                f"📥 Download Link for: {title}\\n\\n{download_link}",
                disable_web_page_preview=True
            )
            logger.info(f"Sent download link for {video_id}")
        
        elif action == 'file':
            # User wants the video file
            await query.edit_message_text(f"⏳ Uploading video...")
            
            try:
                # Upload video to chat
                with open(file_path, 'rb') as video_file:
                    await query.message.reply_video(
                        video=video_file,
                        caption=f"📹 {title}",
                        read_timeout=60,
                        write_timeout=60,
                        connect_timeout=30,
                        pool_timeout=30
                    )
                
                # Update message to show success
                await query.edit_message_text(f"✅ Video uploaded: {title}")
                logger.info(f"Uploaded video file for {video_id}")
                
                # Cleanup
                self.downloader.cleanup_file(file_path)
                
            except Exception as e:
                logger.error(f"Video upload failed: {str(e)}")
                await query.edit_message_text(f"❌ Upload failed: {str(e)}")
        
        # Clean up stored data
        if video_id in context.bot_data['downloads']:
            del context.bot_data['downloads'][video_id]
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors."""
        logger.error(f"Update {update} caused error {context.error}")
    
    def run(self):
        """Start the bot."""
        logger.info("Starting Telegram bot...")
        
        # Create application
        application = Application.builder().token(self.token).build()
        
        # Register handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_message))
        application.add_handler(CallbackQueryHandler(self.button_callback))  # Handle button clicks
        
        # Register error handler
        application.add_error_handler(self.error_handler)
        
        # Start polling
        logger.info("Bot started successfully!")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point."""
    try:
        # Create and set event loop for Python 3.14+ compatibility
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        bot = TelegramBot()
        bot.run()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please create a .env file with TELEGRAM_BOT_TOKEN")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        try:
            loop.close()
        except:
            pass


if __name__ == '__main__':
    main()

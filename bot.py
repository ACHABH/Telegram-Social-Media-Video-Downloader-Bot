"""
Telegram Social Media Video Downloader Bot
Main application file handling Telegram bot interactions.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from url_handler import URLHandler
from preference_parser import PreferenceParser
from response_formatter import ResponseFormatter
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
        self.preference_parser = PreferenceParser()
        self.response_formatter = ResponseFormatter()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = (
            "🎥 *Telegram Social Media Video Downloader Bot*\n\n"
            "Send me links from:\n"
            "• YouTube\n"
            "• Facebook\n"
            "• X (Twitter)\n"
            "• Instagram\n"
            "• TikTok\n\n"
            "*Usage:*\n"
            "• Just send a link → Get download link\n"
            "• Add 'send file' → Get video as file\n"
            "• Add 'send link' → Get download link\n\n"
            "You can send multiple links at once!"
        )
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_message = (
            "*How to use:*\n\n"
            "1. Send me a video URL from supported platforms\n"
            "2. Optionally add 'send file' or 'send link'\n"
            "3. I'll process and respond with JSON\n\n"
            "*Examples:*\n"
            "`https://youtube.com/watch?v=abc123`\n"
            "`https://tiktok.com/@user/video/123 send file`\n"
            "`https://instagram.com/p/abc send link`"
        )
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def process_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Process incoming messages containing video URLs.
        
        Purpose: Extract URLs, download videos, and respond with structured JSON.
        Required inputs: Message text containing at least one valid URL.
        """
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
        
        results = []
        
        # Process each URL
        for url_info in urls:
            url = url_info['url']
            platform = url_info['platform']
            
            logger.info(f"Processing {platform} URL: {url}")
            
            # Determine user preference
            preference = self.preference_parser.parse_preference(message_text, url)
            
            # Download video
            download_result = self.downloader.download_video(url, platform)
            
            # Validation: Check if download succeeded
            if not download_result['success']:
                logger.warning(f"Download failed for {url}: {download_result['error']}")
                results.append(
                    self.response_formatter.create_error_response(url, download_result['error'])
                )
                continue
            
            # Handle based on preference
            if preference == 'file':
                # Upload as Telegram file
                try:
                    file_path = download_result['file_path']
                    
                    # Send video file to user
                    with open(file_path, 'rb') as video_file:
                        sent_message = await update.message.reply_video(
                            video=video_file,
                            caption=f"📹 {download_result.get('title', 'Video')}"
                        )
                    
                    # Get file_id from sent message
                    file_id = sent_message.video.file_id
                    
                    # Cleanup downloaded file
                    self.downloader.cleanup_file(file_path)
                    
                    # Validation: Verify file was uploaded
                    logger.info(f"File uploaded successfully: {file_id}")
                    
                    results.append(
                        self.response_formatter.create_success_response(
                            url, 'file', video_file=file_id
                        )
                    )
                
                except Exception as e:
                    logger.error(f"File upload failed: {str(e)}")
                    results.append(
                        self.response_formatter.create_error_response(
                            url, f"File upload failed: {str(e)}"
                        )
                    )
            
            else:  # preference == 'link' (default)
                # Generate download link
                file_path = download_result['file_path']
                filename = Path(file_path).name
                
                # Use web server URL if configured, otherwise use file path
                if self.web_server_url:
                    download_link = f"{self.web_server_url.rstrip('/')}/{filename}"
                else:
                    # For local testing, provide the file path
                    # In production, this should be a proper web URL
                    download_link = f"file:///{file_path}"
                
                # Validation: Verify link was generated
                logger.info(f"Download link generated: {download_link}")
                
                results.append(
                    self.response_formatter.create_success_response(
                        url, 'link', download_link=download_link
                    )
                )
        
        # Format and send JSON response
        json_response = self.response_formatter.format_response(results)
        
        # Delete processing message
        await processing_msg.delete()
        
        # Send JSON response
        await update.message.reply_text(f"```json\n{json_response}\n```", parse_mode='Markdown')
        
        logger.info(f"Completed processing {len(results)} URLs")
    
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
        
        # Register error handler
        application.add_error_handler(self.error_handler)
        
        # Start polling
        logger.info("Bot started successfully!")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point."""
    try:
        bot = TelegramBot()
        bot.run()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please create a .env file with TELEGRAM_BOT_TOKEN")
    except Exception as e:
        logger.error(f"Fatal error: {e}")


if __name__ == '__main__':
    main()

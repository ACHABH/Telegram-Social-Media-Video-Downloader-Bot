# Telegram Social Media Video Downloader Bot

A feature-rich Telegram bot that downloads videos from YouTube, Facebook, X (Twitter), Instagram, and TikTok with an interactive button interface.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **Multi-Platform Support**: Download from YouTube, Facebook, X/Twitter, Instagram, and TikTok
- **Interactive Interface**: Choose between download link or direct video upload using inline buttons
- **YouTube Shorts Support**: Optimized for all YouTube formats including Shorts
- **No Keyword Commands**: Just send a link and click a button - that's it!
- **Async Architecture**: Fast, non-blocking downloads
- **Clean & Simple**: Minimal setup required

## 🎬 Demo

1. Send a video URL to the bot
2. Bot downloads and shows two buttons:
   - 📥 **Get Link** - Receive a download link
   - 📹 **Send Video** - Get the video directly in chat
3. Click your preferred option!

## 📋 Prerequisites

- Python 3.8 or higher
- A Telegram bot token from [@BotFather](https://t.me/botfather)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/telegram-video-downloader-bot.git
cd telegram-video-downloader-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Your Bot

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your bot token:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
DOWNLOAD_DIR=./downloads
WEB_SERVER_URL=
```

**Getting your bot token:**
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the instructions
3. Copy the token provided and paste it in `.env`

### 4. Run the Bot

```bash
python bot.py
```

You should see:
```
INFO - Starting Telegram bot...
INFO - Bot started successfully!
```

## 🎯 Usage

### Basic Usage

Simply send a video URL from any supported platform:

```
https://youtube.com/watch?v=dQw4w9WgXcQ
https://youtube.com/shorts/abc123
https://tiktok.com/@user/video/123456789
https://instagram.com/reel/abc123/
https://twitter.com/user/status/123456789
```

The bot will:
1. Download the video
2. Show you two buttons
3. Deliver based on your choice!

### Supported Platforms

| Platform | URL Examples |
|----------|-------------|
| **YouTube** | `youtube.com/watch?v=...`<br>`youtu.be/...`<br>`youtube.com/shorts/...` |
| **TikTok** | `tiktok.com/@user/video/...`<br>`vm.tiktok.com/...` |
| **Instagram** | `instagram.com/p/...`<br>`instagram.com/reel/...` |
| **X (Twitter)** | `twitter.com/user/status/...`<br>`x.com/user/status/...` |
| **Facebook** | `facebook.com/.../videos/...`<br>`fb.watch/...` |

## 🛠️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | - | Your Telegram bot token |
| `DOWNLOAD_DIR` | ❌ No | `./downloads` | Directory for downloaded videos |
| `WEB_SERVER_URL` | ❌ No | - | Base URL for serving download links (for production) |

### Download Directory

Downloaded videos are temporarily stored in the `downloads` directory. Files are automatically cleaned up after being sent to users when using "Send Video" mode.

### Production Deployment

For production use with "Get Link" mode, you should:

1. Set up a web server to serve the downloaded files
2. Configure `WEB_SERVER_URL` to point to your server
3. Ensure the `downloads` directory is accessible via HTTP

**Example with nginx:**
```nginx
location /downloads/ {
    alias /path/to/bot/downloads/;
    autoindex off;
}
```

Then set in `.env`:
```env
WEB_SERVER_URL=https://yourdomain.com/downloads
```

## 📁 Project Structure

```
telegram-video-downloader-bot/
├── bot.py                      # Main bot application
├── url_handler.py              # URL extraction and platform detection
├── video_downloader.py         # Video download logic using yt-dlp
├── preference_parser.py        # Legacy preference parser (kept for compatibility)
├── response_formatter.py       # Legacy JSON formatter (kept for compatibility)
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🧪 Testing

The project includes unit tests for core components:

```bash
# Run all tests
pytest -v

# Run specific tests
pytest test_url_handler.py -v
pytest test_preference_parser.py -v
pytest test_response_formatter.py -v
```

## 🐛 Troubleshooting

### Bot doesn't respond
- Verify your bot token in `.env`
- Ensure the bot process is running
- Check logs for error messages

### YouTube download fails
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Some videos may be geo-restricted or private
- YouTube Shorts require yt-dlp 2024.11.18 or newer

### Video upload timeout
- Large videos (>50MB) may exceed Telegram's limits
- Use "Get Link" mode for large files
- Check your internet connection speed

### Python 3.14 Compatibility
The bot is fully compatible with Python 3.14. If you encounter event loop errors:
- The code includes `asyncio.new_event_loop()` setup
- Requires `python-telegram-bot>=22.5`

## 🔧 Dependencies

- **python-telegram-bot** (>=22.5) - Telegram Bot API wrapper
- **yt-dlp** (>=2024.11.18) - Universal video downloader
- **python-dotenv** (>=1.0.0) - Environment variable management

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

## ⚠️ Disclaimer

This bot is for educational and personal use only. Please respect:
- Copyright laws and content creator rights
- Platform terms of service
- Fair use guidelines

The developers are not responsible for misuse of this software.

## 🙏 Acknowledgments

- [python-telegram-bot](https://python-telegram-bot.org/) - Excellent Telegram Bot framework
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Powerful video downloader
- The open-source community

## 📧 Support

If you encounter any issues or have questions:
- Open an [issue](https://github.com/yourusername/telegram-video-downloader-bot/issues)
- Check existing issues for solutions
- Review the troubleshooting section above

## ⭐ Show Your Support

If you find this project helpful, please give it a ⭐️!

---

**Made with ❤️ for the open-source community**

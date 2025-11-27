# Telegram Social Media Video Downloader Bot

A Telegram bot that downloads videos from YouTube, Facebook, X (Twitter), Instagram, and TikTok with structured JSON responses.

## Features

- 📹 **Multi-Platform Support**: YouTube, Facebook, X/Twitter, Instagram, TikTok
- 🎯 **Flexible Delivery**: Send as file or download link based on user preference
- 📦 **Batch Processing**: Handle multiple URLs in a single message
- 🔄 **Structured Responses**: JSON-formatted responses for programmatic use
- ⚡ **Fast Downloads**: Powered by yt-dlp for reliable video extraction

## Installation

### Prerequisites

- Python 3.8 or higher
- A Telegram bot token from [@BotFather](https://t.me/botfather)

### Setup

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Edit `.env` and add your bot token:
     ```
     TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
     ```

4. **Run the bot**:
   ```bash
   python bot.py
   ```

## Usage

### Basic Commands

- `/start` - Welcome message and quick guide
- `/help` - Detailed usage instructions

### Sending Links

Simply send a video URL to the bot:

**Default behavior (download link):**
```
https://youtube.com/watch?v=abc123
```

**Request file upload:**
```
https://tiktok.com/@user/video/123 send file
```

**Request download link:**
```
https://instagram.com/reel/abc123 send link
```

**Multiple URLs:**
```
https://youtube.com/watch?v=abc send file
https://tiktok.com/@user/video/456 send link
```

## Response Format

The bot responds with JSON arrays. Each element represents a processed video link:

### Success Response (File)
```json
{
  "status": "success",
  "input_link": "https://youtube.com/watch?v=abc123",
  "type": "file",
  "video_file": "AgADBAADzmoxG64Z2Ug7KbD",
  "download_link": null,
  "error": null
}
```

### Success Response (Link)
```json
{
  "status": "success",
  "input_link": "https://tiktok.com/@user/video/xyz",
  "type": "link",
  "video_file": null,
  "download_link": "https://myserver.com/download/xyz.mp4",
  "error": null
}
```

### Error Response
```json
{
  "status": "error",
  "input_link": "https://unsupported.com/video",
  "type": null,
  "video_file": null,
  "download_link": null,
  "error": "Unsupported URL or platform."
}
```

## Supported Platforms

| Platform | URL Format Examples |
|----------|-------------------|
| YouTube | `youtube.com/watch?v=...`, `youtu.be/...`, `youtube.com/shorts/...` |
| Facebook | `facebook.com/.../videos/...`, `fb.watch/...` |
| X (Twitter) | `twitter.com/.../status/...`, `x.com/.../status/...` |
| Instagram | `instagram.com/p/...`, `instagram.com/reel/...` |
| TikTok | `tiktok.com/@.../video/...`, `vm.tiktok.com/...` |

## Testing

Run the test suite to verify functionality:

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest -v

# Run specific test file
pytest test_url_handler.py -v
pytest test_preference_parser.py -v
pytest test_response_formatter.py -v
```

## Configuration

### Environment Variables

- `TELEGRAM_BOT_TOKEN` (required): Your Telegram bot token
- `DOWNLOAD_DIR` (optional): Directory for downloaded videos (default: `./downloads`)
- `WEB_SERVER_URL` (optional): Base URL for serving download links in production

### Production Deployment

For production use:

1. **Set up a web server** to serve downloaded files
2. **Configure `WEB_SERVER_URL`** in your `.env` file
3. **Consider using a process manager** like `systemd`, `pm2`, or `supervisor`
4. **Implement cleanup routines** for old downloaded files

Example systemd service:
```ini
[Unit]
Description=Telegram Video Downloader Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 /path/to/bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Project Structure

```
├── bot.py                      # Main bot application
├── url_handler.py              # URL extraction and validation
├── preference_parser.py        # User preference detection
├── response_formatter.py       # JSON response formatting
├── video_downloader.py         # Video download handler
├── test_url_handler.py         # Tests for URL handler
├── test_preference_parser.py   # Tests for preference parser
├── test_response_formatter.py  # Tests for response formatter
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Troubleshooting

### Bot doesn't respond
- Check if bot token is correctly set in `.env`
- Verify bot is running with `python bot.py`
- Check logs for error messages

### Download fails
- Some platforms may have geographic restrictions
- Private or age-restricted videos may not be downloadable
- Check that yt-dlp is up to date: `pip install --upgrade yt-dlp`

### File upload errors
- Large files (>50MB) may fail on Telegram
- Use "send link" mode for large videos
- Check available disk space

## License

This project is open source and available for educational and personal use.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Disclaimer

This bot is for educational purposes. Respect copyright laws and platform terms of service when downloading content.

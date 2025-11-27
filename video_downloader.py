"""
Video Downloader Module
Downloads videos from supported platforms using yt-dlp.
"""

import os
import tempfile
from pathlib import Path
from typing import Dict, Optional
import yt_dlp


class VideoDownloader:
    """Handles video downloading from various platforms."""
    
    def __init__(self, download_dir: Optional[str] = None):
        """
        Initialize the video downloader.
        
        Args:
            download_dir: Directory to save downloaded videos (defaults to temp)
        """
        if download_dir:
            self.download_dir = Path(download_dir)
            self.download_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.download_dir = Path(tempfile.gettempdir()) / 'telegram_bot_downloads'
            self.download_dir.mkdir(parents=True, exist_ok=True)
    
    def download_video(self, url: str, platform: str) -> Dict:
        """
        Download video from the given URL.
        
        Args:
            url: Video URL
            platform: Platform name (youtube, facebook, twitter, instagram, tiktok)
            
        Returns:
            Dictionary with 'success' (bool), 'file_path' (str), 'error' (str) keys
        """
        try:
            # Configure yt-dlp options
            # NOTE: NOT specifying 'format' to let yt-dlp auto-select the best available
            # This avoids "Requested format is not available" errors
            ydl_opts = {
                'outtmpl': str(self.download_dir / '%(id)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Verify file exists
                if not os.path.exists(filename):
                    return {
                        'success': False,
                        'file_path': None,
                        'error': 'Download completed but file not found'
                    }
                
                return {
                    'success': True,
                    'file_path': filename,
                    'error': None,
                    'title': info.get('title', 'video'),
                    'duration': info.get('duration', 0)
                }
        
        except yt_dlp.utils.DownloadError as e:
            return {
                'success': False,
                'file_path': None,
                'error': f'Download failed: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'file_path': None,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def cleanup_file(self, file_path: str) -> None:
        """
        Delete a downloaded file.
        
        Args:
            file_path: Path to the file to delete
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass  # Silently fail on cleanup errors

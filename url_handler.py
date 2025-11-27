"""
URL Handler Module
Extracts and validates URLs from user messages.
Supports: YouTube, Facebook, X (Twitter), Instagram, TikTok
"""

import re
from typing import List, Dict
from urllib.parse import urlparse


class URLHandler:
    """Handles URL extraction and validation for supported platforms."""
    
    SUPPORTED_PLATFORMS = {
        'youtube': [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/shorts/[\w-]+',
        ],
        'facebook': [
            r'(?:https?://)?(?:www\.)?facebook\.com/.*?/videos/\d+',
            r'(?:https?://)?(?:www\.)?fb\.watch/[\w-]+',
        ],
        'twitter': [
            r'(?:https?://)?(?:www\.)?twitter\.com/\w+/status/\d+',
            r'(?:https?://)?(?:www\.)?x\.com/\w+/status/\d+',
        ],
        'instagram': [
            r'(?:https?://)?(?:www\.)?instagram\.com/(?:p|reel)/[\w-]+',
        ],
        'tiktok': [
            r'(?:https?://)?(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+',
            r'(?:https?://)?(?:vm\.)?tiktok\.com/[\w-]+',
        ],
    }
    
    @classmethod
    def extract_urls(cls, text: str) -> List[Dict[str, str]]:
        """
        Extract all valid URLs from the given text.
        
        Args:
            text: User message text
            
        Returns:
            List of dictionaries containing 'url' and 'platform' keys
        """
        # General URL pattern to find all potential URLs
        url_pattern = r'https?://[^\s]+'
        potential_urls = re.findall(url_pattern, text)
        
        # Also check for URLs without protocol
        no_protocol_pattern = r'(?:www\.)?(?:youtube\.com|youtu\.be|facebook\.com|fb\.watch|twitter\.com|x\.com|instagram\.com|tiktok\.com|vm\.tiktok\.com)[^\s]+'
        potential_urls.extend(re.findall(no_protocol_pattern, text))
        
        extracted = []
        seen = set()
        
        for url in potential_urls:
            # Normalize URL
            if not url.startswith('http'):
                url = 'https://' + url
            
            # Avoid duplicates
            if url in seen:
                continue
            
            platform = cls.identify_platform(url)
            if platform:
                extracted.append({
                    'url': url,
                    'platform': platform
                })
                seen.add(url)
        
        return extracted
    
    @classmethod
    def identify_platform(cls, url: str) -> str:
        """
        Identify which platform a URL belongs to.
        
        Args:
            url: The URL to check
            
        Returns:
            Platform name or empty string if unsupported
        """
        for platform, patterns in cls.SUPPORTED_PLATFORMS.items():
            for pattern in patterns:
                if re.match(pattern, url, re.IGNORECASE):
                    return platform
        return ''
    
    @classmethod
    def is_valid_url(cls, url: str) -> bool:
        """
        Check if URL is from a supported platform.
        
        Args:
            url: The URL to validate
            
        Returns:
            True if supported, False otherwise
        """
        return bool(cls.identify_platform(url))

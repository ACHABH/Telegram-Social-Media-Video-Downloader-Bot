"""
Unit tests for URL Handler module
"""

import pytest
from url_handler import URLHandler


class TestURLHandler:
    """Test cases for URL extraction and validation."""
    
    def test_extract_youtube_url(self):
        """Test YouTube URL extraction."""
        text = "Check out this video https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        urls = URLHandler.extract_urls(text)
        
        assert len(urls) == 1
        assert urls[0]['platform'] == 'youtube'
        assert 'youtube.com' in urls[0]['url']
    
    def test_extract_youtube_short_url(self):
        """Test YouTube short URL."""
        text = "Short link: https://youtu.be/dQw4w9WgXcQ"
        urls = URLHandler.extract_urls(text)
        
        assert len(urls) == 1
        assert urls[0]['platform'] == 'youtube'
    
    def test_extract_tiktok_url(self):
        """Test TikTok URL extraction."""
        text = "https://www.tiktok.com/@user/video/1234567890"
        urls = URLHandler.extract_urls(text)
        
        assert len(urls) == 1
        assert urls[0]['platform'] == 'tiktok'
    
    def test_extract_instagram_url(self):
        """Test Instagram URL extraction."""
        text = "Cool reel: https://www.instagram.com/reel/ABC123xyz/"
        urls = URLHandler.extract_urls(text)
        
        assert len(urls) == 1
        assert urls[0]['platform'] == 'instagram'
    
    def test_extract_twitter_url(self):
        """Test Twitter/X URL extraction."""
        text1 = "https://twitter.com/user/status/1234567890"
        text2 = "https://x.com/user/status/1234567890"
        
        urls1 = URLHandler.extract_urls(text1)
        urls2 = URLHandler.extract_urls(text2)
        
        assert len(urls1) == 1
        assert urls1[0]['platform'] == 'twitter'
        assert len(urls2) == 1
        assert urls2[0]['platform'] == 'twitter'
    
    def test_extract_facebook_url(self):
        """Test Facebook URL extraction."""
        text = "https://www.facebook.com/username/videos/1234567890"
        urls = URLHandler.extract_urls(text)
        
        assert len(urls) == 1
        assert urls[0]['platform'] == 'facebook'
    
    def test_extract_multiple_urls(self):
        """Test extraction of multiple URLs."""
        text = (
            "Check out these videos: "
            "https://youtube.com/watch?v=abc123 and "
            "https://tiktok.com/@user/video/456789"
        )
        urls = URLHandler.extract_urls(text)
        
        assert len(urls) == 2
        assert urls[0]['platform'] == 'youtube'
        assert urls[1]['platform'] == 'tiktok'
    
    def test_no_urls(self):
        """Test message with no URLs."""
        text = "This is just a regular message with no links"
        urls = URLHandler.extract_urls(text)
        
        assert len(urls) == 0
    
    def test_unsupported_url(self):
        """Test unsupported URL."""
        text = "https://www.example.com/video"
        urls = URLHandler.extract_urls(text)
        
        assert len(urls) == 0
    
    def test_url_without_protocol(self):
        """Test URL without https:// protocol."""
        text = "Check youtube.com/watch?v=abc123"
        urls = URLHandler.extract_urls(text)
        
        assert len(urls) == 1
        assert urls[0]['platform'] == 'youtube'
    
    def test_identify_platform(self):
        """Test platform identification."""
        assert URLHandler.identify_platform("https://youtube.com/watch?v=test") == 'youtube'
        assert URLHandler.identify_platform("https://tiktok.com/@user/video/123") == 'tiktok'
        assert URLHandler.identify_platform("https://example.com") == ''
    
    def test_is_valid_url(self):
        """Test URL validation."""
        assert URLHandler.is_valid_url("https://youtube.com/watch?v=test") == True
        assert URLHandler.is_valid_url("https://example.com") == False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

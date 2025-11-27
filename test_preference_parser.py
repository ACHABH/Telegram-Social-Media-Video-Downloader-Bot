"""
Unit tests for Preference Parser module
"""

import pytest
from preference_parser import PreferenceParser


class TestPreferenceParser:
    """Test cases for preference detection."""
    
    def test_send_file_preference(self):
        """Test 'send file' keyword detection."""
        text = "https://youtube.com/watch?v=abc send file"
        url = "https://youtube.com/watch?v=abc"
        
        preference = PreferenceParser.parse_preference(text, url)
        assert preference == 'file'
    
    def test_send_link_preference(self):
        """Test 'send link' keyword detection."""
        text = "https://youtube.com/watch?v=abc send link"
        url = "https://youtube.com/watch?v=abc"
        
        preference = PreferenceParser.parse_preference(text, url)
        assert preference == 'link'
    
    def test_default_preference(self):
        """Test default preference when no keyword."""
        text = "https://youtube.com/watch?v=abc"
        url = "https://youtube.com/watch?v=abc"
        
        preference = PreferenceParser.parse_preference(text, url)
        assert preference == 'link'  # Default is 'link'
    
    def test_case_insensitive(self):
        """Test case-insensitive matching."""
        text1 = "https://youtube.com/watch?v=abc SEND FILE"
        text2 = "https://youtube.com/watch?v=abc Send Link"
        url = "https://youtube.com/watch?v=abc"
        
        pref1 = PreferenceParser.parse_preference(text1, url)
        pref2 = PreferenceParser.parse_preference(text2, url)
        
        assert pref1 == 'file'
        assert pref2 == 'link'
    
    def test_multiple_urls_different_preferences(self):
        """Test different preferences for multiple URLs."""
        text = "https://youtube.com/1 send file and https://tiktok.com/2 send link"
        
        url1 = "https://youtube.com/1"
        url2 = "https://tiktok.com/2"
        
        pref1 = PreferenceParser.parse_preference(text, url1)
        pref2 = PreferenceParser.parse_preference(text, url2)
        
        assert pref1 == 'file'
        assert pref2 == 'link'
    
    def test_global_preference(self):
        """Test global preference at start of message."""
        text = "send file https://youtube.com/watch?v=abc"
        url = "https://youtube.com/watch?v=abc"
        
        preference = PreferenceParser.parse_preference(text, url)
        assert preference == 'file'
    
    def test_preference_with_extra_text(self):
        """Test preference detection with surrounding text."""
        text = "Please send file for this link: https://youtube.com/watch?v=abc thanks!"
        url = "https://youtube.com/watch?v=abc"
        
        preference = PreferenceParser.parse_preference(text, url)
        assert preference == 'file'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

"""
Preference Parser Module
Detects user preferences for video delivery method.
"""

import re
from typing import Optional


class PreferenceParser:
    """Parses user messages to determine video delivery preference."""
    
    @staticmethod
    def parse_preference(text: str, url: str) -> str:
        """
        Determine user's preference for how to receive the video.
        
        Args:
            text: Complete user message
            url: The specific URL being processed
            
        Returns:
            'file', 'link', or 'default' (which defaults to 'link')
        """
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Find the position of the URL in the text
        try:
            url_pos = text_lower.index(url.lower())
        except ValueError:
            # URL not found in text, use global preference
            url_pos = 0
        
        # Look for preference keywords after the URL
        # This allows per-URL preferences
        text_after_url = text_lower[url_pos:]
        
        # Check for "send file" or similar
        if re.search(r'\bsend\s+file\b', text_after_url):
            return 'file'
        
        # Check for "send link" or similar
        if re.search(r'\bsend\s+link\b', text_after_url):
            return 'link'
        
        # Also check the entire message for global preference
        if re.search(r'\bsend\s+file\b', text_lower):
            return 'file'
        
        if re.search(r'\bsend\s+link\b', text_lower):
            return 'link'
        
        # Default to 'link' when no preference specified
        return 'link'

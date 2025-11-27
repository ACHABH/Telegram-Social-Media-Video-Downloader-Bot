"""
Response Formatter Module
Creates structured JSON responses according to the specified format.
"""

import json
from typing import List, Dict, Optional


class ResponseFormatter:
    """Formats bot responses as structured JSON."""
    
    @staticmethod
    def format_response(results: List[Dict]) -> str:
        """
        Format results into JSON string.
        
        Args:
            results: List of result dictionaries
            
        Returns:
            JSON string formatted according to specification
        """
        return json.dumps(results, indent=2, ensure_ascii=False)
    
    @staticmethod
    def create_success_response(
        input_link: str,
        response_type: str,
        video_file: Optional[str] = None,
        download_link: Optional[str] = None
    ) -> Dict:
        """
        Create a success response object.
        
        Args:
            input_link: Original URL from user
            response_type: 'file' or 'link'
            video_file: Telegram file_id (if type is 'file')
            download_link: Download URL (if type is 'link')
            
        Returns:
            Formatted success response dictionary
        """
        return {
            "status": "success",
            "input_link": input_link,
            "type": response_type,
            "video_file": video_file,
            "download_link": download_link,
            "error": None
        }
    
    @staticmethod
    def create_error_response(input_link: str, error_message: str) -> Dict:
        """
        Create an error response object.
        
        Args:
            input_link: Original URL from user
            error_message: Description of the error
            
        Returns:
            Formatted error response dictionary
        """
        return {
            "status": "error",
            "input_link": input_link,
            "type": None,
            "video_file": None,
            "download_link": None,
            "error": error_message
        }

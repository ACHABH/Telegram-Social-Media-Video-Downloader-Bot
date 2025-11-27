"""
Unit tests for Response Formatter module
"""

import pytest
import json
from response_formatter import ResponseFormatter


class TestResponseFormatter:
    """Test cases for JSON response formatting."""
    
    def test_create_success_response_file(self):
        """Test success response with file type."""
        response = ResponseFormatter.create_success_response(
            input_link="https://youtube.com/watch?v=abc",
            response_type="file",
            video_file="AgADBAADzmoxG64Z2Ug7KbD"
        )
        
        assert response['status'] == 'success'
        assert response['input_link'] == "https://youtube.com/watch?v=abc"
        assert response['type'] == 'file'
        assert response['video_file'] == "AgADBAADzmoxG64Z2Ug7KbD"
        assert response['download_link'] is None
        assert response['error'] is None
    
    def test_create_success_response_link(self):
        """Test success response with link type."""
        response = ResponseFormatter.create_success_response(
            input_link="https://tiktok.com/@user/video/123",
            response_type="link",
            download_link="https://myserver.com/download/video123"
        )
        
        assert response['status'] == 'success'
        assert response['type'] == 'link'
        assert response['download_link'] == "https://myserver.com/download/video123"
        assert response['video_file'] is None
        assert response['error'] is None
    
    def test_create_error_response(self):
        """Test error response creation."""
        response = ResponseFormatter.create_error_response(
            input_link="https://invalid.com/video",
            error_message="Unsupported URL or platform."
        )
        
        assert response['status'] == 'error'
        assert response['input_link'] == "https://invalid.com/video"
        assert response['type'] is None
        assert response['video_file'] is None
        assert response['download_link'] is None
        assert response['error'] == "Unsupported URL or platform."
    
    def test_format_response_single(self):
        """Test formatting single result to JSON."""
        results = [
            ResponseFormatter.create_success_response(
                input_link="https://youtube.com/watch?v=abc",
                response_type="link",
                download_link="https://server.com/video.mp4"
            )
        ]
        
        json_str = ResponseFormatter.format_response(results)
        parsed = json.loads(json_str)
        
        assert isinstance(parsed, list)
        assert len(parsed) == 1
        assert parsed[0]['status'] == 'success'
    
    def test_format_response_multiple(self):
        """Test formatting multiple results to JSON."""
        results = [
            ResponseFormatter.create_success_response(
                input_link="https://youtube.com/watch?v=abc",
                response_type="link",
                download_link="https://server.com/video1.mp4"
            ),
            ResponseFormatter.create_error_response(
                input_link="https://invalid.com/video",
                error_message="Unsupported platform"
            )
        ]
        
        json_str = ResponseFormatter.format_response(results)
        parsed = json.loads(json_str)
        
        assert len(parsed) == 2
        assert parsed[0]['status'] == 'success'
        assert parsed[1]['status'] == 'error'
    
    def test_response_schema_compliance(self):
        """Test that response matches exact schema."""
        response = ResponseFormatter.create_success_response(
            input_link="https://youtube.com/watch?v=test",
            response_type="file",
            video_file="FILE123"
        )
        
        required_keys = ['status', 'input_link', 'type', 'video_file', 'download_link', 'error']
        assert all(key in response for key in required_keys)
        assert len(response) == len(required_keys)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

"""
UI Services Module

This module handles the business logic for UI operations, including
file handling, API communication, and data processing.
Provides clean separation between UI components and business logic.
"""
import requests
import tempfile
import mimetypes
from io import BytesIO
from typing import Dict, Any, Optional, Tuple


class CVUploadService:
    """Handles CV file upload and processing operations."""
    
    def __init__(self, api_base_url: str = "http://127.0.0.1:8000"):
        self.api_base_url = api_base_url
    
    def upload_cv_file(self, file_path: str, file_name: str) -> Tuple[bool, str, str]:
        """
        Upload a CV file to the API for processing.
        
        Args:
            file_path: Path to the file to upload
            file_name: Name of the file
            
        Returns:
            Tuple of (success, message, cv_text)
        """
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
            
            # Determine MIME type
            mime_type, _ = mimetypes.guess_type(file_name)
            if not mime_type:
                if file_name.lower().endswith('.pdf'):
                    mime_type = 'application/pdf'
                elif file_name.lower().endswith('.txt'):
                    mime_type = 'text/plain'
                else:
                    mime_type = 'application/octet-stream'
            
            # Prepare file for upload
            files = {"file": (file_name, BytesIO(file_data), mime_type)}
            
            # Make API request
            response = requests.post(f"{self.api_base_url}/api/v1/upload/cv", files=files)
            data = response.json()
            
            if response.status_code == 200 and data.get("success", False):
                return True, "CV uploaded successfully", data.get("text", "")
            else:
                return False, data.get("message", "Unknown error occurred"), ""
                
        except Exception as ex:
            return False, f"Error processing file: {str(ex)}", ""


class FeedbackService:
    """Handles feedback generation requests."""
    
    def __init__(self, api_base_url: str = "http://127.0.0.1:8000"):
        self.api_base_url = api_base_url
    
    def get_feedback(self, cv_text: str, feedback_type: str) -> Tuple[bool, str]:
        """
        Request feedback for a CV text.
        
        Args:
            cv_text: The CV text content
            feedback_type: Type of feedback ('grammar', 'experience', 'layout')
            
        Returns:
            Tuple of (success, feedback_text)
        """
        try:
            response = requests.post(
                f"{self.api_base_url}/api/v1/feedback",
                json={"text": cv_text, "feedback_type": feedback_type}
            )
            
            if response.status_code == 200:
                data = response.json()
                return True, data.get("feedback", "")
            else:
                return False, f"Error: {response.text}"
                
        except Exception as e:
            return False, f"Error: {str(e)}"


class UIStateManager:
    """Manages the application's UI state."""
    
    def __init__(self):
        self.cv_text: str = ""
        self.is_cv_loaded: bool = False
        self.current_feedback: str = ""
        self.last_feedback_type: Optional[str] = None
    
    def set_cv_text(self, text: str) -> None:
        """Set the current CV text and update state."""
        self.cv_text = text
        self.is_cv_loaded = bool(text.strip())
    
    def clear_cv(self) -> None:
        """Clear the current CV and reset state."""
        self.cv_text = ""
        self.is_cv_loaded = False
        self.current_feedback = ""
        self.last_feedback_type = None
    
    def set_feedback(self, feedback: str, feedback_type: str) -> None:
        """Set the current feedback and type."""
        self.current_feedback = feedback
        self.last_feedback_type = feedback_type
    
    def can_get_feedback(self) -> bool:
        """Check if feedback can be requested (CV is loaded)."""
        return self.is_cv_loaded

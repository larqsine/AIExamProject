"""
Event Handlers Module

This module contains event handling logic for UI interactions.
Separates event handling from UI component definitions and business logic.
"""
import flet as ft
from typing import Callable
from .services import CVUploadService, FeedbackService, UIStateManager


class FileUploadHandler:
    """Handles file upload events and operations."""
    
    def __init__(self, 
                 upload_service: CVUploadService,
                 state_manager: UIStateManager,
                 status_text: ft.Text,
                 cv_preview: ft.Text,
                 cv_preview_container: ft.Container,
                 feedback_container: ft.Column):
        self.upload_service = upload_service
        self.state_manager = state_manager
        self.status_text = status_text
        self.cv_preview = cv_preview
        self.cv_preview_container = cv_preview_container
        self.feedback_container = feedback_container
    
    def handle_file_picked(self, e: ft.FilePickerResultEvent) -> None:
        """Handle file picker result event."""
        if not e.files or len(e.files) == 0:
            return
        
        file = e.files[0]
        self._update_status(f"Uploading: {file.name}...", ft.Colors.BLUE)
        
        # Upload file using service
        success, message, cv_text = self.upload_service.upload_cv_file(file.path, file.name)
        
        if success:
            # Update state and UI on success
            self.state_manager.set_cv_text(cv_text)
            self.cv_preview.value = cv_text
            self.feedback_container.visible = True
            self._update_status("CV uploaded successfully. Select feedback type below.", ft.Colors.GREEN)
        else:
            # Handle error
            self.state_manager.clear_cv()
            self._update_status(f"Error: {message}", ft.Colors.RED)
        
        # Update UI components
        self._update_ui_components()
    
    def _update_status(self, message: str, color: str = ft.Colors.BLACK) -> None:
        """Update status text with message and color."""
        self.status_text.value = message
        self.status_text.color = color
        self.status_text.update()
    
    def _update_ui_components(self) -> None:
        """Update all relevant UI components."""
        self.cv_preview_container.update()
        self.feedback_container.update()


class FeedbackHandler:
    """Handles feedback request events."""
    
    def __init__(self,
                 feedback_service: FeedbackService,
                 state_manager: UIStateManager,
                 feedback_status: ft.Text,
                 feedback_result: ft.Text,
                 feedback_result_container: ft.Container):
        self.feedback_service = feedback_service
        self.state_manager = state_manager
        self.feedback_status = feedback_status
        self.feedback_result = feedback_result
        self.feedback_result_container = feedback_result_container
    
    def get_feedback(self, feedback_type: str) -> None:
        """Handle feedback request for a specific type."""
        if not self.state_manager.can_get_feedback():
            self._update_feedback_status("Please upload a CV first", ft.Colors.RED)
            return
        
        self._update_feedback_status(f"Getting {feedback_type} feedback...", ft.Colors.BLUE)
        
        # Request feedback using service
        success, feedback = self.feedback_service.get_feedback(
            self.state_manager.cv_text, 
            feedback_type
        )
        
        if success:
            # Update state and UI on success
            self.state_manager.set_feedback(feedback, feedback_type)
            self.feedback_result.value = feedback
            self.feedback_result_container.visible = True
            self._update_feedback_status(f"{feedback_type.capitalize()} feedback ready!", ft.Colors.GREEN)
        else:
            # Handle error
            self._update_feedback_status(feedback, ft.Colors.RED)
        
        # Update UI components
        self._update_feedback_ui()
    
    def _update_feedback_status(self, message: str, color: str = ft.Colors.BLACK) -> None:
        """Update feedback status text."""
        self.feedback_status.value = message
        self.feedback_status.color = color
        self.feedback_status.update()
    
    def _update_feedback_ui(self) -> None:
        """Update feedback-related UI components."""
        self.feedback_result_container.update()

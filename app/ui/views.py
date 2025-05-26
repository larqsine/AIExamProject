"""
Main Views Module

This module contains the main view definitions for the AI CV Helper application.
Refactored to use proper separation of concerns with dedicated service and handler classes.
"""
import flet as ft
from .components import (
    create_title_section, create_upload_button, create_status_text,
    create_cv_preview_section, create_feedback_buttons, 
    create_feedback_result_container, create_main_container
)
from .services import CVUploadService, FeedbackService, UIStateManager
from .handlers import FileUploadHandler, FeedbackHandler


def main_view(page: ft.Page) -> None:
    """
    Create and configure the main application view.
    
    This function sets up the entire UI using a clean architecture pattern:
    - Components handle UI element creation
    - Services manage business logic and API communication  
    - Handlers manage event processing
    - State manager tracks application state
    """
    # Configure page properties
    _configure_page(page)
    
    # Initialize services and state management
    upload_service = CVUploadService()
    feedback_service = FeedbackService()
    state_manager = UIStateManager()
    
    # Create UI components
    ui_components = _create_ui_components()
    
    # Set up file picker
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    
    # Initialize event handlers
    upload_handler = FileUploadHandler(
        upload_service=upload_service,
        state_manager=state_manager,
        status_text=ui_components['status_text'],
        cv_preview=ui_components['cv_preview'],
        cv_preview_container=ui_components['cv_preview_container'],
        feedback_container=ui_components['feedback_container']
    )
    
    feedback_handler = FeedbackHandler(
        feedback_service=feedback_service,
        state_manager=state_manager,
        feedback_status=ui_components['feedback_status'],
        feedback_result=ui_components['feedback_result'],
        feedback_result_container=ui_components['feedback_result_container']
    )
    
    # Connect event handlers
    file_picker.on_result = upload_handler.handle_file_picked
    
    # Configure upload button to use file picker
    ui_components['upload_button'].on_click = lambda _: file_picker.pick_files(
        allowed_extensions=["pdf", "txt"],
        allow_multiple=False
    )
    
    # Configure feedback buttons
    feedback_buttons = create_feedback_buttons(feedback_handler.get_feedback)
    
    # Build the complete UI layout
    main_content = _build_main_layout(ui_components, feedback_buttons)
    
    # Add to page
    page.add(create_main_container(main_content))


def _configure_page(page: ft.Page) -> None:
    """Configure page-level properties."""
    page.title = "AI CV Helper"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO


def _create_ui_components() -> dict:
    """Create all UI components and return them in a dictionary."""
    # Create individual components
    status_text = create_status_text()
    upload_button = create_upload_button(None)  # on_click will be set later
    
    cv_preview_title, cv_preview, cv_preview_container = create_cv_preview_section()
    feedback_status, feedback_result, feedback_result_container = create_feedback_result_container()
    
    # Create feedback container structure
    feedback_container = ft.Column(
        [
            ft.Divider(),
            ft.Text("Get Feedback:", size=16, weight=ft.FontWeight.BOLD),
            ft.Container(),  # Placeholder for feedback buttons
            feedback_status,
            feedback_result_container  
        ],
        visible=False
    )
    
    return {
        'status_text': status_text,
        'upload_button': upload_button,
        'cv_preview_title': cv_preview_title,
        'cv_preview': cv_preview,
        'cv_preview_container': cv_preview_container,
        'feedback_status': feedback_status,
        'feedback_result': feedback_result,
        'feedback_result_container': feedback_result_container,
        'feedback_container': feedback_container
    }


def _build_main_layout(ui_components: dict, feedback_buttons: ft.Row) -> ft.Column:
    """Build the main layout structure."""
    # Update feedback container with actual buttons
    ui_components['feedback_container'].controls[2] = feedback_buttons
    
    return ft.Column(
        [
            *create_title_section().controls,
            ui_components['upload_button'],
            ui_components['status_text'],
            ft.Container(height=20),
            ui_components['cv_preview_title'],
            ui_components['cv_preview_container'], 
            ui_components['feedback_container']
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

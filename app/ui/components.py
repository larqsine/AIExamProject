"""
UI Components Module

This module contains reusable UI components for the CV Helper application.
Separates the UI component definitions from the main view logic.
"""
import flet as ft
from typing import Callable, Optional


def create_title_section() -> ft.Column:
    """Create the main title and subtitle section."""
    return ft.Column([
        ft.Text("AI CV Helper", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("Upload your CV for AI-powered feedback", size=16),
        ft.Container(height=20),
    ])


def create_upload_button(on_click: Callable) -> ft.ElevatedButton:
    """Create the file upload button."""
    return ft.ElevatedButton(
        "Upload CV (PDF/TXT)",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=on_click
    )


def create_status_text() -> ft.Text:
    """Create the status text component."""
    return ft.Text("", size=14)


def create_cv_preview_section() -> tuple[ft.Text, ft.Text, ft.Container]:
    """Create the CV preview section components."""
    title = ft.Text("CV Preview:", size=16, weight=ft.FontWeight.BOLD)
    preview_text = ft.Text("", size=12, selectable=True)
    
    container = ft.Container(
        content=ft.Column(
            [preview_text],
            scroll=ft.ScrollMode.AUTO 
        ),
        height=200,  
        width=700,   
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=5,
        padding=10,
        bgcolor=ft.Colors.GREY_50
    )
    
    return title, preview_text, container


def create_feedback_buttons(get_feedback_callback: Callable) -> ft.Row:
    """Create the feedback type selection buttons."""
    grammar_button = ft.ElevatedButton(
        "Grammar Check",
        icon=ft.Icons.SPELLCHECK,
        on_click=lambda _: get_feedback_callback("grammar")
    )
    
    experience_button = ft.ElevatedButton(
        "Experience Check",
        icon=ft.Icons.WORK,
        on_click=lambda _: get_feedback_callback("experience")
    )
    
    layout_button = ft.ElevatedButton(
        "Layout Check",
        icon=ft.Icons.VIEW_COMPACT,
        on_click=lambda _: get_feedback_callback("layout") 
    )
    
    return ft.Row(
        [grammar_button, experience_button, layout_button],
        alignment=ft.MainAxisAlignment.CENTER
    )


def create_feedback_result_container() -> tuple[ft.Text, ft.Text, ft.Container]:
    """Create the feedback result display components."""
    status = ft.Text("", size=14)
    result_text = ft.Text("", size=14, selectable=True)
    
    container = ft.Container(
        content=ft.Column(
            [result_text],
            scroll=ft.ScrollMode.AUTO  
        ),
        height=300,  
        width=700,   
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=5,
        padding=10,
        bgcolor=ft.Colors.GREY_50,
        visible=False  
    )
    
    return status, result_text, container


def create_main_container(content: ft.Column) -> ft.Container:
    """Create the main application container with styling."""
    return ft.Container(
        content=content,
        padding=20,
        width=800,
        border_radius=10,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK12
        )
    )

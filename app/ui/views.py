import flet as ft
import requests
import json
from io import BytesIO
import tempfile
import os
from typing import Dict, Any, List, Optional
import mimetypes

def main_view(page: ft.Page):
    page.title = "AI CV Helper"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO  
    
    cv_text = ""
    
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    
    def handle_file_picked(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            file = e.files[0]
            status_text.value = f"Uploading: {file.name}..."
            status_text.update()
            
            try:
                with open(file.path, "rb") as f:
                    file_data = f.read()
                
                mime_type, _ = mimetypes.guess_type(file.name)
                if not mime_type:
                    if file.name.lower().endswith('.pdf'):
                        mime_type = 'application/pdf'
                    elif file.name.lower().endswith('.txt'):
                        mime_type = 'text/plain'
                    else:
                        mime_type = 'application/octet-stream'  
                
                files = {"file": (file.name, BytesIO(file_data), mime_type)}
                response = requests.post("http://127.0.0.1:8000/api/v1/upload/cv", files=files)
                data = response.json()
                
                if response.status_code == 200 and data.get("success", False):
                    nonlocal cv_text
                    cv_text = data.get("text", "")
                    cv_preview.value = cv_text  
                    feedback_container.visible = True
                    status_text.value = "CV uploaded successfully. Select feedback type below."
                    status_text.color = ft.Colors.GREEN
                else:
                    status_text.value = f"Error: {data.get('message', 'Unknown error')}"
                    status_text.color = ft.Colors.RED
                    
                status_text.update()
                cv_preview_container.update()
                feedback_container.update()
                    
            except Exception as ex:
                status_text.value = f"Error processing file: {str(ex)}"
                status_text.color = ft.Colors.RED
                status_text.update()
    
    file_picker.on_result = handle_file_picked
    def get_feedback(feedback_type: str):
        if not cv_text:
            status_text.value = "Please upload a CV first"
            status_text.color = ft.Colors.RED
            status_text.update()
            return
            
        feedback_status.value = f"Getting {feedback_type} feedback..."
        feedback_status.update()
        
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/v1/feedback",
                json={"text": cv_text, "feedback_type": feedback_type}
            )
            
            if response.status_code == 200:
                data = response.json()
                feedback_result.value = data.get("feedback", "")
                feedback_result_container.visible = True
                feedback_status.value = f"{feedback_type.capitalize()} feedback ready!"
                feedback_status.color = ft.Colors.GREEN
            else:
                feedback_status.value = f"Error: {response.text}"
                feedback_status.color = ft.Colors.RED
                
            feedback_status.update()
            feedback_result_container.update()
            
        except Exception as e:
            feedback_status.value = f"Error: {str(e)}"
            feedback_status.color = ft.Colors.RED
            feedback_status.update()
    
    title = ft.Text("AI CV Helper", size=32, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("Upload your CV for AI-powered feedback", size=16)
    
    upload_button = ft.ElevatedButton(
        "Upload CV (PDF/TXT)",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(
            allowed_extensions=["pdf", "txt"],
            allow_multiple=False
        )
    )
    
    status_text = ft.Text("", size=14)
    
    cv_preview_title = ft.Text("CV Preview:", size=16, weight=ft.FontWeight.BOLD)
    cv_preview = ft.Text("", size=12, selectable=True)
    
    cv_preview_container = ft.Container(
        content=ft.Column(
            [cv_preview],
            scroll=ft.ScrollMode.AUTO 
        ),
        height=200,  
        width=700,   
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=5,
        padding=10,
        bgcolor=ft.Colors.GREY_50
    )
    
    
    feedback_status = ft.Text("", size=14)
    feedback_result = ft.Text("", size=14, selectable=True)
    
    feedback_result_container = ft.Container(
        content=ft.Column(
            [feedback_result],
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
    
    grammar_button = ft.ElevatedButton(
        "Grammar Check",
        icon=ft.Icons.SPELLCHECK,
        on_click=lambda _: get_feedback("grammar")
    )
    
    experience_button = ft.ElevatedButton(
        "Experience Check",
        icon=ft.Icons.WORK,
        on_click=lambda _: get_feedback("experience")
    )
    
    layout_button = ft.ElevatedButton(
        "Layout Check",
        icon=ft.Icons.VIEW_COMPACT,
        on_click=lambda _: get_feedback("layout") 
    )
    
    feedback_buttons = ft.Row(
        [grammar_button, experience_button, layout_button],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    feedback_container = ft.Column(
        [
            ft.Divider(),
            ft.Text("Get Feedback:", size=16, weight=ft.FontWeight.BOLD),
            feedback_buttons,
            feedback_status,
            feedback_result_container  
        ],
        visible=False
    )
    
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    title,
                    subtitle,
                    ft.Container(height=20),
                    upload_button,
                    status_text,
                    ft.Container(height=20),
                    cv_preview_title,
                    cv_preview_container, 
                    feedback_container
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
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
    )

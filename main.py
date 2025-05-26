"""
Main Application Entry Point

This module serves as the entry point for the AI CV Helper application.
It sets up and runs both the FastAPI backend and Flet frontend concurrently.

Architecture:
- FastAPI: Provides REST API endpoints for CV processing and feedback
- Flet: Creates the desktop GUI application
- Threading: Runs both services simultaneously for seamless user experience

The application follows a clean architecture pattern with:
- API layer for backend services
- UI layer for frontend components  
- LLM layer for AI processing
- Proper separation of concerns throughout
"""
import flet as ft
from fastapi import FastAPI
import threading
import uvicorn

from app.api.routes import router
from app.ui.views import main_view

# Create FastAPI application instance with metadata
app = FastAPI(
    title="AI CV Helper",
    description="AI-powered CV analysis and feedback system using LangChain and Ollama",
    version="1.0.0"
)

# Include API routes with version prefix
app.include_router(router)


def main(page: ft.Page):
    """
    Initialize and configure the main Flet application page.
    
    This function serves as the entry point for the GUI application,
    setting up the page configuration and loading the main view.
    
    Args:
        page: The Flet page object to configure
    """
    page.title = "AI CV Helper"
    main_view(page)


def run_api():
    """
    Start the FastAPI server in a separate thread.
    
    This allows the API to run concurrently with the GUI application,
    providing backend services while the user interacts with the frontend.
    """
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


if __name__ == "__main__":
    # Start the API server in a daemon thread
    # Daemon threads automatically terminate when the main program exits
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Start the Flet GUI application
    # This will block until the GUI is closed by the user
    ft.app(target=main)
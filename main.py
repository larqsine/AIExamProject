import flet as ft
from fastapi import FastAPI
import threading

# Import your application components
from app.api.routes import routes
from app.ui.views import views

# Create FastAPI app
app = FastAPI(title="AI CV Helper")

# Register API routes
app.include_router(router)

# Define Flet UI main function
def main(page: ft.Page):
    page.title = "AI CV Helper"
    main_view(page)

# Function to run FastAPI server
def run_api():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# If running directly, start both API and UI
if __name__ == "__main__":
    # Start API server in a separate thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Start Flet UI
    ft.app(target=main)
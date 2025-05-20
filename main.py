import flet as ft
from fastapi import FastAPI
import threading
import uvicorn

from app.api.routes import router
from app.ui.views import main_view

app = FastAPI(title="AI CV Helper")

app.include_router(router)

def main(page: ft.Page):
    page.title = "AI CV Helper"
    main_view(page)

def run_api():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    ft.app(target=main)
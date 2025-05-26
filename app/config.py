"""
Application Configuration Module

This module centralizes all configuration settings for the AI CV Helper application.
Provides a single source of truth for application settings and makes the codebase
more maintainable and configurable.
"""
import os
from typing import List


class AppConfig:
    """Main application configuration class."""
    
    # API Configuration
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_BASE_URL: str = f"http://{API_HOST}:{API_PORT}"
    API_VERSION: str = "v1"
    
    # File Upload Configuration
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "txt"]
    MAX_FILE_SIZE_MB: int = 10
    
    # UI Configuration
    APP_TITLE: str = "AI CV Helper"
    APP_DESCRIPTION: str = "Upload your CV for AI-powered feedback"
    
    # Page Layout Configuration
    MAIN_CONTAINER_WIDTH: int = 800
    CV_PREVIEW_HEIGHT: int = 200
    CV_PREVIEW_WIDTH: int = 700
    FEEDBACK_RESULT_HEIGHT: int = 300
    FEEDBACK_RESULT_WIDTH: int = 700
    
    # CV Validation Configuration
    MIN_CV_LENGTH: int = 50  # Minimum character count for valid CV
    MIN_CV_INDICATORS: int = 2  # Minimum CV indicators required
    
    # RAG Configuration
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    RAG_CHUNK_SIZE: int = 100
    RAG_CHUNK_OVERLAP: int = 0
    RAG_SIMILARITY_RESULTS: int = 3
    
    # Model Configuration
    DEFAULT_TEMPERATURE: float = 0.2
    DEFAULT_TOP_P: float = 0.1
    DEFAULT_TOP_K: int = 40
    DEFAULT_REPEAT_PENALTY: float = 1.2
    
    # Feedback Types
    FEEDBACK_TYPES: List[str] = ["grammar", "experience", "layout"]
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ENABLE_VERBOSE_LOGGING: bool = os.getenv("VERBOSE_LOGGING", "false").lower() == "true"


class ModelConfig:
    """Model-specific configuration settings."""
    
    # Grammar Model Configuration
    GRAMMAR_MODEL_NAME: str = "codellama:7b-instruct"
    GRAMMAR_TEMPERATURE: float = 0.2
    GRAMMAR_TOP_P: float = 0.1
    GRAMMAR_TOP_K: int = 40
    GRAMMAR_REPEAT_PENALTY: float = 1.2
    
    # Experience Model Configuration
    EXPERIENCE_MODEL_NAME: str = "codellama:7b-instruct"
    EXPERIENCE_TEMPERATURE: float = 0.1
    EXPERIENCE_TOP_P: float = 0.2
    EXPERIENCE_TOP_K: int = 40
    EXPERIENCE_REPEAT_PENALTY: float = 1.1
    
    # Layout Model Configuration
    LAYOUT_MODEL_NAME: str = "wizardcoder:7b-python"
    LAYOUT_TEMPERATURE: float = 0.3
    LAYOUT_STOP_TOKENS: List[str] = ["```"]


class CVGuidelines:
    """CV writing guidelines for RAG system."""
    
    GUIDELINES: List[str] = [
        "CVs should be concise and ideally one to two pages long.",
        "Use bullet points to highlight achievements and responsibilities.",
        "Include quantifiable achievements when possible (e.g., 'Increased sales by 30%').",
        "Customize your CV for each job application.",
        "Use active voice and action verbs (e.g., 'managed', 'led', 'developed').",
        "Ensure consistent formatting throughout the document.",
        "Proofread for grammar and spelling errors.",
        "Include relevant keywords from the job description.",
        "Reverse chronological order is standard for work experience.",
        "Include contact information at the top of your CV.",
        "Avoid personal pronouns (I, me, my).",
        "Focus on relevant experience and skills for the position.",
        "Use a professional email address.",
        "Only include relevant education details.",
        "Highlight transferable skills if changing careers."
    ]


# Create global configuration instances
app_config = AppConfig()
model_config = ModelConfig()
cv_guidelines = CVGuidelines()

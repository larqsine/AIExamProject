"""
API Routes Module

This module defines the FastAPI routes for the AI CV Helper application.
Provides RESTful endpoints for CV upload, processing, and feedback generation.

Key features:
- File upload with validation and CV detection
- Multiple feedback types (grammar, experience, layout)
- Proper error handling and status codes
- Clean separation between API layer and business logic
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import tempfile
from typing import List, Optional

from app.llm.chains import get_grammar_feedback, get_experience_feedback, get_layout_feedback
from app.llm.tools import extract_text_from_pdf, extract_text_from_txt, is_valid_cv

# Create API router with version prefix for future API versioning
router = APIRouter(prefix="/api/v1")


class FeedbackRequest(BaseModel):
    """
    Request model for feedback generation.
    
    Attributes:
        text: The CV text content to analyze
        feedback_type: Type of feedback requested ('grammar', 'experience', 'layout')
    """
    text: str
    feedback_type: str


class FeedbackResponse(BaseModel):
    """
    Response model for feedback generation.
    
    Attributes:
        feedback: The generated feedback text
    """
    feedback: str


@router.post("/upload/cv", response_model=dict)
async def upload_cv(file: UploadFile = File(...)):
    """
    Upload and process a CV file.
    
    This endpoint:
    1. Accepts PDF or TXT files
    2. Extracts text content using appropriate parsers
    3. Validates that the content appears to be a CV
    4. Returns extracted text or appropriate error messages
    
    Args:
        file: The uploaded file (PDF or TXT format)
        
    Returns:
        JSON response with success status, message, and extracted text
        
    Raises:
        HTTPException: For unsupported file formats
    """
    try:
        # Create temporary file for processing
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            content = await file.read()
            temp.write(content)
            temp_path = temp.name

        # Extract text based on file type
        if file.filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(temp_path)
        elif file.filename.lower().endswith('.txt'):
            text = extract_text_from_txt(temp_path)
        else:
            # Clean up and reject unsupported formats
            os.unlink(temp_path)
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file format. Please upload a PDF or TXT file."
            )

        # Clean up temporary file
        os.unlink(temp_path)

        # Validate that the extracted text appears to be a valid CV
        # This prevents processing of non-CV documents
        if not is_valid_cv(text):
            return JSONResponse(
                status_code=400,
                content={
                    "success": False, 
                    "message": "This doesn't appear to be a valid CV/resume. Please upload a proper CV document so I can help you with feedback."
                }
            )

        # Return successful response with extracted text
        return {"success": True, "text": text, "message": "CV uploaded successfully"}

    except Exception as e:
        # Handle any unexpected errors during processing
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Error processing file: {str(e)}"}
        )


@router.post("/feedback", response_model=FeedbackResponse)
async def get_feedback(request: FeedbackRequest):
    """
    Generate specific type of feedback for a CV.
    
    This endpoint routes feedback requests to the appropriate LLM chain
    based on the requested feedback type. Each type uses specialized
    models and prompts for optimal results.
    
    Args:
        request: FeedbackRequest containing CV text and feedback type
        
    Returns:
        FeedbackResponse containing the generated feedback
        
    Raises:
        HTTPException: For invalid feedback types or processing errors
    """
    try:
        # Route to appropriate feedback function based on type
        if request.feedback_type == "grammar":
            feedback = get_grammar_feedback(request.text)
        elif request.feedback_type == "experience":
            feedback = get_experience_feedback(request.text)
        elif request.feedback_type == "layout":
            feedback = get_layout_feedback(request.text)
        else:
            # Reject invalid feedback types
            raise HTTPException(
                status_code=400, 
                detail="Invalid feedback type. Supported types: grammar, experience, layout"
            )

        return {"feedback": feedback}

    except Exception as e:
        # Handle errors during feedback generation
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating feedback: {str(e)}"
        )
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import tempfile
from typing import List, Optional

from app.llm.chains import get_grammar_feedback, get_experience_feedback, get_layout_feedback
from app.llm.tools import extract_text_from_pdf, extract_text_from_txt

router = APIRouter(prefix="/api/v1")


class FeedbackRequest(BaseModel):
    text: str
    feedback_type: str


class FeedbackResponse(BaseModel):
    feedback: str


@router.post("/upload/cv", response_model=dict)
async def upload_cv(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            content = await file.read()
            temp.write(content)
            temp_path = temp.name

        if file.filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(temp_path)
        elif file.filename.lower().endswith('.txt'):
            text = extract_text_from_txt(temp_path)
        else:
            os.unlink(temp_path)
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a PDF or TXT file.")

        os.unlink(temp_path)

        return {"success": True, "text": text, "message": "CV uploaded successfully"}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Error processing file: {str(e)}"}
        )


@router.post("/feedback", response_model=FeedbackResponse)
async def get_feedback(request: FeedbackRequest):
    try:
        if request.feedback_type == "grammar":
            feedback = get_grammar_feedback(request.text)
        elif request.feedback_type == "experience":
            feedback = get_experience_feedback(request.text)
        elif request.feedback_type == "layout":
            feedback = get_layout_feedback(request.text)
        else:
            raise HTTPException(status_code=400, detail="Invalid feedback type")

        return {"feedback": feedback}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating feedback: {str(e)}")
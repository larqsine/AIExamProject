import fitz
from typing import Dict, Any, List
import os
import re

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file"""
    try:
        doc = fitz.open(file_path)
        text = ""
        
        for page in doc:
            text += page.get_text()
            
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        raise e

def extract_text_from_txt(file_path: str) -> str:
    """Extract text from a TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error extracting text from TXT: {str(e)}")
        raise e

def clean_cv_text(text: str) -> str:
    """Clean and normalize CV text"""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,;:\-\'\"()@]', '', text)
    return text.strip()

def identify_cv_sections(text: str) -> Dict[str, str]:
    """Attempt to identify and separate CV sections"""
    sections = {}
    
    section_patterns = {
        "personal_info": r"(?i)(personal\s*information|contact\s*details|profile)",
        "education": r"(?i)(education|academic\s*background|qualifications)",
        "experience": r"(?i)(experience|work\s*experience|employment\s*history|work\s*history)",
        "skills": r"(?i)(skills|technical\s*skills|key\s*skills|competencies)",
        "projects": r"(?i)(projects|personal\s*projects)",
        "references": r"(?i)(references|referees)"
    }
    
    
    current_text = text
    for section, pattern in section_patterns.items():
        matches = re.search(pattern, current_text)
        if matches:
            start_pos = matches.start()
            section_text = current_text[start_pos:]
            sections[section] = section_text
    
    return sections

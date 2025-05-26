"""
Document Processing and Validation Tools

This module provides utilities for extracting, processing, and validating CV documents.
It includes smart CV detection algorithms to ensure only valid CVs are processed.

Key features:
- PDF and TXT text extraction
- Intelligent CV validation using regex patterns
- Text cleaning and normalization
- CV section identification (for future enhancements)
"""
import fitz
from typing import Dict, Any, List
import os
import re


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file using PyMuPDF.
    
    This function opens a PDF document and extracts all text content
    from every page, concatenating it into a single string.
    
    Args:
        file_path: Path to the PDF file to process
        
    Returns:
        Extracted text content as a string
        
    Raises:
        Exception: If PDF cannot be opened or processed
    """
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
    """
    Extract text content from a plain text file.
    
    Reads the entire content of a text file using UTF-8 encoding
    to handle international characters properly.
    
    Args:
        file_path: Path to the text file to read
        
    Returns:
        File content as a string
        
    Raises:
        Exception: If file cannot be read or doesn't exist
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error extracting text from TXT: {str(e)}")
        raise e


def clean_cv_text(text: str) -> str:
    """
    Clean and normalize CV text for better processing.
    
    This function performs basic text cleaning operations:
    - Normalizes whitespace (multiple spaces become single space)
    - Removes special characters while preserving common punctuation
    - Strips leading and trailing whitespace
    
    Args:
        text: Raw text content to clean
        
    Returns:
        Cleaned and normalized text
    """
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep common punctuation
    text = re.sub(r'[^\w\s.,;:\-\'\"()@]', '', text)
    return text.strip()


def identify_cv_sections(text: str) -> Dict[str, str]:
    """
    Attempt to identify and separate CV sections using pattern matching.
    
    This function uses regex patterns to identify common CV sections
    like personal information, education, experience, etc. This can be
    useful for future enhancements that need to analyze specific sections.
    
    Args:
        text: CV text content to analyze
        
    Returns:
        Dictionary mapping section names to their content
        
    Note:
        This is a basic implementation that could be enhanced with
        more sophisticated NLP techniques for better accuracy.
    """
    sections = {}
    
    # Define patterns for common CV sections
    section_patterns = {
        "personal_info": r"(?i)(personal\s*information|contact\s*details|profile)",
        "education": r"(?i)(education|academic\s*background|qualifications)",
        "experience": r"(?i)(experience|work\s*experience|employment\s*history|work\s*history)",
        "skills": r"(?i)(skills|technical\s*skills|key\s*skills|competencies)",
        "projects": r"(?i)(projects|personal\s*projects)",
        "references": r"(?i)(references|referees)"
    }
    
    # Search for each section pattern and extract content
    current_text = text
    for section, pattern in section_patterns.items():
        matches = re.search(pattern, current_text)
        if matches:
            start_pos = matches.start()
            section_text = current_text[start_pos:]
            sections[section] = section_text
    
    return sections

def is_valid_cv(text: str) -> bool:
    """
    Determine if the extracted text appears to be a valid CV/resume.
    
    This function implements intelligent CV detection using a scoring system
    based on regex pattern matching. It looks for common CV indicators while
    checking for patterns that suggest the document is NOT a CV.
    
    The algorithm works by:
    1. Checking for minimum text length (50 characters)
    2. Scoring positive CV indicators (email, sections, keywords)
    3. Scoring negative non-CV indicators (books, invoices, etc.)
    4. Requiring at least 2 CV indicators and fewer non-CV indicators
    
    Common CV indicators include:
    - Contact information (email, phone)
    - Standard CV sections (experience, education, skills)
    - Professional keywords and action verbs
    - Academic and job-related terminology
    
    Non-CV indicators include:
    - Book/manual content (chapters, table of contents)
    - Letters (dear, sincerely)
    - Financial documents (invoice, payment)
    - Legal documents (contract, agreement)
    
    Args:
        text: The extracted document text to validate
        
    Returns:
        True if the text appears to be a valid CV, False otherwise
        
    Example:
        >>> is_valid_cv("John Doe john@email.com Experience: Software Developer")
        True
        >>> is_valid_cv("Chapter 1: Introduction to Python Programming")
        False
    """
    # Basic validation: ensure minimum content length
    if not text or len(text.strip()) < 50:
        return False
    
    text_lower = text.lower()
    
    # CV indicators - patterns commonly found in CVs/resumes
    cv_indicators = [
        # Contact information patterns
        r'\b\w+@\w+\.\w+\b',  # Email pattern (e.g., john@email.com)
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # Phone pattern (e.g., 555-123-4567)
        
        # CV section headers
        r'\b(experience|work experience|employment)\b',
        r'\b(education|academic|qualification|degree)\b',
        r'\b(skills|technical skills|competencies)\b',
        r'\b(contact|personal|profile)\b',
        
        # Common CV keywords
        r'\b(resume|curriculum vitae|cv)\b',
        r'\b(university|college|bachelor|master|phd)\b',
        r'\b(company|corporation|organization|firm)\b',
        r'\b(manager|developer|engineer|analyst|specialist)\b',
        r'\b(responsible for|managed|led|developed|created)\b'
    ]
    
    # Non-CV indicators - patterns that suggest it's NOT a CV
    non_cv_indicators = [
        r'\b(chapter|page \d+|table of contents)\b',  # Book/document structure
        r'\b(article|abstract|introduction|conclusion)\b',  # Academic paper
        r'\b(dear|sincerely|yours faithfully)\b',  # Formal letter
        r'\b(invoice|receipt|bill|payment)\b',  # Financial document
        r'\b(contract|agreement|terms and conditions)\b',  # Legal document
        r'\b(manual|instructions|tutorial|guide)\b'  # Manual/guide content
    ]
    
    # Count pattern matches for scoring
    cv_score = 0
    non_cv_score = 0
    
    # Score positive CV indicators
    for pattern in cv_indicators:
        if re.search(pattern, text_lower):
            cv_score += 1
    
    # Score negative non-CV indicators
    for pattern in non_cv_indicators:
        if re.search(pattern, text_lower):
            non_cv_score += 1
    
    # Decision logic: must have sufficient CV indicators and fewer non-CV indicators
    # This ensures we catch genuine CVs while rejecting other document types
    return cv_score >= 2 and non_cv_score < cv_score

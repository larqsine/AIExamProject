"""
LangChain Integration Module

This module implements the core LangChain functionality for the AI CV Helper application.
It provides three main feedback types using RAG (Retrieval-Augmented Generation):
- Grammar and language feedback
- Work experience feedback  
- Layout and structure feedback

The module uses:
- LangChain for prompt management and chain execution
- FAISS vector store for CV guideline retrieval (RAG implementation)
- HuggingFace embeddings for semantic similarity
- Conversation memory for context retention
- Specialized Ollama models for different feedback types
"""
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os
import tempfile
from typing import List, Dict, Any

from .modelRegistry import get_model_for_task
from .modelTask import ModelTask

# Global conversation memory for maintaining context across interactions
# This enables the AI to remember previous feedback and conversations
cv_memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True
)

# Comprehensive CV writing guidelines database
# These guidelines form the knowledge base for RAG (Retrieval-Augmented Generation)
# The AI retrieves relevant guidelines based on the type of feedback requested
cv_guidelines = [
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


def initialize_rag():
    """
    Initialize the RAG (Retrieval-Augmented Generation) system.
    
    This function:
    1. Creates a temporary file with CV guidelines
    2. Loads and splits the guidelines into chunks
    3. Creates embeddings using HuggingFace model
    4. Builds a FAISS vector store for similarity search
    5. Cleans up temporary files
    
    Returns:
        FAISS vectorstore containing embedded CV guidelines
    """
    # Create temporary file with guidelines content
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("\n".join(cv_guidelines))
        file_path = f.name
    
    # Load and split the guidelines into manageable chunks
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store for semantic search
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    # Clean up temporary file
    os.unlink(file_path)
    
    return vectorstore

# Initialize the global RAG vector store
vectorstore = initialize_rag()


def get_relevant_guidelines(query: str, k: int = 3) -> List[str]:
    """
    Retrieve relevant CV guidelines based on semantic similarity to the query.
    
    This function implements the "Retrieval" part of RAG by finding the most
    relevant guidelines for the specific type of feedback being requested.
    
    Args:
        query: The search query (e.g., "grammar mistakes in CV")
        k: Number of most relevant guidelines to return
        
    Returns:
        List of relevant guideline strings
    """
    docs = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]


def get_grammar_feedback(cv_text: str) -> str:
    """
    Generate grammar and language feedback for a CV.
    
    This function uses:
    - Specialized grammar model from the model registry
    - RAG to retrieve relevant grammar guidelines
    - Custom prompt template for grammar-focused feedback
    
    Args:
        cv_text: The CV content to analyze
        
    Returns:
        Detailed grammar and language feedback
    """
    # Get the specialized model for grammar tasks
    model = get_model_for_task(ModelTask.GRAMMAR)
    
    # Retrieve relevant guidelines using RAG
    guidelines = get_relevant_guidelines("grammar mistakes in CV")
    guidelines_text = "\n".join(guidelines)
    
    # Create specialized prompt template for grammar feedback
    prompt = PromptTemplate(
        input_variables=["cv_text", "guidelines"],
        template="""
        You are a detail-oriented and helpful CV coach. You specialize in improving grammar and language use.
        
        Review the CV below and provide constructive feedback on grammar, spelling, and language use.
        Focus on clarity and professionalism. Be specific and point out exact issues.
        
        Reference these CV writing guidelines:
        {guidelines}
        
        CV TEXT:
        {cv_text}
        
        GRAMMAR AND LANGUAGE FEEDBACK:
        """
    )
    
    # Execute the chain with verbose logging for debugging
    chain = LLMChain(llm=model, prompt=prompt, verbose=True)
    response = chain.predict(cv_text=cv_text, guidelines=guidelines_text)
    return response


def get_experience_feedback(cv_text: str) -> str:
    """
    Generate work experience feedback for a CV.
    
    This function focuses on how work experience is presented, including:
    - Use of action verbs and quantifiable achievements
    - Relevance and clarity of experience descriptions
    - Professional presentation of career progression
    
    Args:
        cv_text: The CV content to analyze
        
    Returns:
        Detailed work experience feedback
    """
    # Get the specialized model for experience evaluation
    model = get_model_for_task(ModelTask.EXPERIENCE)
    
    # Retrieve guidelines specific to work experience descriptions
    guidelines = get_relevant_guidelines("describing work experience in CV")
    guidelines_text = "\n".join(guidelines)
    
    # Create specialized prompt for experience feedback
    prompt = PromptTemplate(
        input_variables=["cv_text", "guidelines"],
        template="""
        You are a detail-oriented and helpful CV coach. You specialize in improving work experience descriptions.
        
        Review the CV below and provide constructive feedback on how the work experience is presented.
        Focus on achievements, action verbs, clarity, and relevance. Suggest specific improvements.
        
        Reference these CV writing guidelines:
        {guidelines}
        
        CV TEXT:
        {cv_text}
        
        EXPERIENCE SECTION FEEDBACK:
        """
    )
    
    # Execute the experience analysis chain
    chain = LLMChain(llm=model, prompt=prompt, verbose=True)
    response = chain.predict(cv_text=cv_text, guidelines=guidelines_text)
    return response


def get_layout_feedback(cv_text: str) -> str:
    """
    Generate layout and structure feedback for a CV.
    
    This function analyzes:
    - Overall document organization and section order
    - Formatting consistency and readability
    - Structure effectiveness for different CV types
    - Professional presentation standards
    
    Args:
        cv_text: The CV content to analyze
        
    Returns:
        Detailed layout and structure feedback
    """
    # Get the specialized model for layout analysis
    model = get_model_for_task(ModelTask.LAYOUT)
    
    # Retrieve guidelines specific to CV layout and structure
    guidelines = get_relevant_guidelines("CV layout and structure")
    guidelines_text = "\n".join(guidelines)
    
    # Create specialized prompt for layout feedback
    prompt = PromptTemplate(
        input_variables=["cv_text", "guidelines"],
        template="""
        You are a detail-oriented and helpful CV coach. You specialize in improving CV layout and structure.
        
        Review the CV below and provide constructive feedback on its organization, section order, 
        and overall structure. Suggest specific improvements to make the CV more effective.
        
        Reference these CV writing guidelines:
        {guidelines}
        
        CV TEXT:
        {cv_text}
        
        LAYOUT AND STRUCTURE FEEDBACK:
        """
    )
    
    # Execute the layout analysis chain
    chain = LLMChain(llm=model, prompt=prompt, verbose=True)
    response = chain.predict(cv_text=cv_text, guidelines=guidelines_text)
    return response

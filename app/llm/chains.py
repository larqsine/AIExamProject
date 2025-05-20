from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os
import tempfile
from typing import List, Dict, Any

from .modelRegistry import get_model_for_task
from .modelTask import ModelTask

cv_memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True
)

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
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("\n".join(cv_guidelines))
        file_path = f.name
    
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    os.unlink(file_path)
    
    return vectorstore

vectorstore = initialize_rag()

def get_relevant_guidelines(query: str, k: int = 3) -> List[str]:
    docs = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]

def get_grammar_feedback(cv_text: str) -> str:
    model = get_model_for_task(ModelTask.GRAMMAR)
    
    guidelines = get_relevant_guidelines("grammar mistakes in CV")
    guidelines_text = "\n".join(guidelines)
    
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
    
    chain = LLMChain(llm=model, prompt=prompt, verbose=True)
    response = chain.predict(cv_text=cv_text, guidelines=guidelines_text)
    return response

def get_experience_feedback(cv_text: str) -> str:
    model = get_model_for_task(ModelTask.EXPERIENCE)
    
    guidelines = get_relevant_guidelines("describing work experience in CV")
    guidelines_text = "\n".join(guidelines)
    
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
    
    chain = LLMChain(llm=model, prompt=prompt, verbose=True)
    response = chain.predict(cv_text=cv_text, guidelines=guidelines_text)
    return response

def get_layout_feedback(cv_text: str) -> str:
    model = get_model_for_task(ModelTask.LAYOUT)
    
    guidelines = get_relevant_guidelines("CV layout and structure")
    guidelines_text = "\n".join(guidelines)
    
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
    
    chain = LLMChain(llm=model, prompt=prompt, verbose=True)
    response = chain.predict(cv_text=cv_text, guidelines=guidelines_text)
    return response

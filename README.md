# AI CV Helper

An intelligent CV analysis tool that provides feedback on grammar, experience descriptions, and layout using AI.

## Overview

AI CV Helper uses LLM models via Ollama to analyze and provide constructive feedback on your resume/CV. The application features a user-friendly interface for uploading CVs and receiving detailed feedback on different aspects.

## Features

- Upload CV files (PDF or TXT format)
- Receive feedback on grammar and language usage
- Get suggestions for improving work experience descriptions
- Receive layout and structure recommendations
- RAG-based system using CV writing guidelines
- Conversation memory to maintain context

## Requirements

- Python 3.9+
- Ollama installed locally with llama3 and/or codellama models
- HuggingFace embeddings

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AIExamProject.git
   cd AIExamProject
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Install Ollama:
   - Follow instructions at [Ollama.ai](https://ollama.ai) to install Ollama
   - Pull the required models:
     ```bash
     ollama pull llama3
     ollama pull codellama:7b-instruct
     ollama pull wizardcoder:7b-python
     ```

## Running the Application

1. Make sure Ollama is running in the background:
   ```bash
   ollama serve
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. The application will start both:
   - Flet UI: Available at http://localhost:8550 (default)
   - FastAPI backend: Running at http://127.0.0.1:8000

## Usage Guide

1. Open the application in your browser
2. Click "Upload CV" to select your CV file (PDF or TXT)
3. Once uploaded, select the type of feedback you want:
   - Grammar Check: Reviews language, grammar, and spelling
   - Experience Check: Analyzes how work experience is presented
   - Layout Check: Reviews organization and structure

## Project Structure

```
AIExamProject/
├── app/
│   ├── api/            # FastAPI endpoints
│   ├── llm/            # LangChain and LLM components
│   │   ├── chains.py   # LangChain chains for CV analysis
│   │   └── tools.py    # Utility tools for text extraction
│   └── ui/             # Flet UI components
├── tests/              # Unit tests
├── main.py            # Application entry point
├── requirements.txt   # Dependencies
└── README.md          # This file
```

## Customizing Models

You can modify the model configuration in `app/llm/modelRegistry.py` to use different Ollama models or adjust parameters like temperature for different feedback styles.

## License

[MIT License](LICENSE)

# Installation and Setup Guide

This document provides detailed instructions for setting up the AI CV Helper application.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)
- Ollama installed on your system

## Step 1: Install Ollama

1. Visit [Ollama.ai](https://ollama.ai) and follow the installation instructions for your operating system
2. After installation, open a terminal/command prompt and pull the required models:

```bash
# Pull Llama3 model
ollama pull llama3

# Pull CodeLlama model
ollama pull codellama:7b-instruct

# Pull WizardCoder model
ollama pull wizardcoder:7b-python
```

## Step 2: Clone or Download the Repository

```bash
git clone https://github.com/yourusername/AIExamProject.git
cd AIExamProject
```

## Step 3: Create and Activate a Virtual Environment

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

## Step 4: Install Dependencies

Install all required packages using pip:

```bash
pip install -r requirements.txt
```

This will install:
- flet (for UI)
- fastapi (for API)
- uvicorn (ASGI server)
- langchain (for LLM orchestration)
- faiss-cpu (for vector storage)
- pymupdf (for PDF processing)
- And other dependencies

### Note on promptfoo

The `promptfoo` package might cause installation issues as it's primarily a Node.js package. If you encounter the error "No matching distribution found for promptfoo>=0.21.0", use one of these solutions:

1. Install dependencies without promptfoo:
   ```bash
   pip install -r requirements.txt --skip-failed-builds
   ```

2. Install promptfoo using npm (requires Node.js):
   ```bash
   npm install -g promptfoo
   ```

3. Modify requirements.txt to remove the promptfoo line

## Step 5: Verify Installation

To verify that all components are correctly installed:

1. Ensure Ollama is running:
   ```bash
   ollama serve
   ```

2. Test Ollama models:
   ```bash
   ollama run llama3 "Hello, how are you?"
   ```

3. Check Python packages:
   ```bash
   python -c "import flet, fastapi, langchain; print('All packages installed!')"
   ```

## Troubleshooting

### Common Issues:

1. **Ollama Connection Error**:
   - Ensure Ollama is running with `ollama serve`
   - Check that it's accessible at http://localhost:11434

2. **Missing Dependencies**:
   - If you encounter import errors, try installing the specific package:
     ```bash
     pip install package_name
     ```

3. **HuggingFace Model Download Issues**:
   - If you experience issues downloading embeddings models, ensure you have internet connectivity
   - Try manually downloading with:
     ```bash
     python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
     ```

4. **Port Already in Use**:
   - If port 8000 or 8550 is already in use, modify the port in `main.py`

5. **promptfoo Installation Error**:
   - promptfoo is primarily a Node.js tool, not a Python package
   - Install it separately using npm: `npm install -g promptfoo`
   - Or remove it from requirements.txt if not needed immediately

For additional help, please open an issue on the GitHub repository.

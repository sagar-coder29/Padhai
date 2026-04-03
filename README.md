# Padhai

An AI-powered study assistant that helps you learn from PDF documents using local LLM.

## Features

- **PDF Upload**: Upload any PDF document for study
- **Text Extraction**: Automatically extracts text from PDF files
- **AI-Powered Q&A**: Ask questions about your study material and get instant answers
- **Local LLM**: Runs entirely on your machine using Ollama

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai/) installed and running

## Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd padhai
```

2. **Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Start Ollama**

Make sure Ollama is running with the gemma model:
```bash
ollama serve
ollama pull gemma4:e4b
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Start the development server**
```bash
python manage.py runserver
```

7. **Open in browser**
Navigate to `http://localhost:8000`

## Usage

1. Click "Choose File" to select a PDF document
2. Click "Upload PDF" to process the document
3. Enter your question in the text field
4. Click "Ask" to get an AI-generated answer based on the PDF content

## Tech Stack

- **Backend**: Django 4.2+
- **PDF Processing**: pdfplumber, PyPDF2
- **AI Model**: Gemma via Ollama
- **Frontend**: HTML, JavaScript (vanilla)

## Project Structure

```
padhai/
├── padhai/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                # Main application
│   ├── views.py         # API endpoints
│   ├── urls.py
│   └── templates/       # HTML templates
├── manage.py
└── requirements.txt
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/api/upload-pdf/` | POST | Upload and process PDF |
| `/api/ask/` | POST | Ask a question about the PDF |

## License

MIT License

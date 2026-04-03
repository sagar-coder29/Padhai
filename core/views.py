import requests
import pdfplumber
import PyPDF2
import io
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

OLLAMA_CONFIG = {
    "model": "gemma4:e4b",
    "baseUrl": "http://localhost:11434/v1",
    "apiKey": "ollama"
}


def extract_text_from_pdf(pdf_file):
    pdf_bytes = pdf_file.read()
    text = ""

    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    text += f"[Page {i+1} - no text extracted]\n"
    except Exception as e:
        pass

    if not text.strip():
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            text = f"Error: {str(e)}"

    return text.strip() if text else "No readable text found in PDF"


def ask_gemma(question, context):
    max_context = 3000
    if len(context) > max_context:
        context = context[:max_context] + "..."

    try:
        response = requests.post(
            f"{OLLAMA_CONFIG['baseUrl']}/chat/completions",
            headers={
                "Authorization": f"Bearer {OLLAMA_CONFIG['apiKey']}",
                "Content-Type": "application/json"
            },
            json={
                "model": OLLAMA_CONFIG["model"],
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful study assistant. Answer questions based only on the provided study material."
                    },
                    {
                        "role": "user",
                        "content": f"Study Material:\n{context}\n\nQuestion: {question}"
                    }
                ],
                "stream": False
            },
            timeout=60,
        )
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}. Make sure Ollama is running with: ollama serve"


def index(request):
    return render(request, "index.html")


@csrf_exempt
def upload_pdf(request):
    if request.method == "POST" and request.FILES.get("pdf"):
        pdf_file = request.FILES["pdf"]
        context = extract_text_from_pdf(pdf_file)
        request.session["pdf_context"] = context
        return JsonResponse({
            "success": True, 
            "text_length": len(context),
            "preview": context[:500] if len(context) > 500 else context
        })
    return JsonResponse({"success": False, "error": "No PDF provided"})


@csrf_exempt
def ask_question(request):
    if request.method == "POST":
        question = request.POST.get("question", "")
        context = request.session.get("pdf_context", "")

        if not context or context == "No readable text found in PDF":
            return JsonResponse({"success": False, "error": "Please upload a PDF with text (not scanned images)"})

        if not question:
            return JsonResponse({"success": False, "error": "Please enter a question"})

        answer = ask_gemma(question, context)
        return JsonResponse({"success": True, "answer": answer})

    return JsonResponse({"success": False, "error": "Invalid request"})

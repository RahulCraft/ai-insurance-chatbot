from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import Document, Chat
import PyPDF2


# -------------------------------
# UI
# -------------------------------
def chat_ui(request):
    return render(request, 'chat.html')


# -------------------------------
# FILE UPLOAD + TEXT EXTRACTION
# -------------------------------
@api_view(['POST'])
def upload_document(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file uploaded ❌"})

    # SAVE FILE
    doc = Document.objects.create(file=file)

    # -------------------------------
    # EXTRACT TEXT FROM PDF
    # -------------------------------
    text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(doc.file.path)

        for page in pdf_reader.pages:
            text += page.extract_text() or ""

    except Exception as e:
        return Response({"error": f"PDF read error: {str(e)}"})

    # SAVE EXTRACTED TEXT
    doc.extracted_text = text
    doc.save()

    return Response({
        "message": "File uploaded & text extracted ✅"
    })


# -------------------------------
# CHAT (SEARCH FROM DOCUMENT)
# -------------------------------
@api_view(['POST'])
def chat(request):
    user_msg = request.data.get("message")

    if not user_msg:
        return Response({"response": "Please ask something ❗"})

    # GET LAST UPLOADED DOCUMENT
    doc = Document.objects.last()

    if not doc or not doc.extracted_text:
        return Response({"response": "No document found ❗ Please upload a file first."})

    # -------------------------------
    # SIMPLE SEARCH LOGIC
    # -------------------------------
    text = doc.extracted_text.lower()
    query = user_msg.lower()

    # find matching sentences
    sentences = text.split(".")
    matched = []

    for sentence in sentences:
        if query in sentence:
            matched.append(sentence.strip())

    # -------------------------------
    # RESPONSE LOGIC
    # -------------------------------
    if matched:
        bot_response = ". ".join(matched[:3])  # top 3 matches
    else:
        bot_response = "Sorry 😢 I could not find answer in document."

    # SAVE CHAT
    Chat.objects.create(
        user_message=user_msg,
        bot_response=bot_response
    )

    return Response({
        "response": bot_response
    })
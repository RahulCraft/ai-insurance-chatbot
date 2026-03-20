import PyPDF2
import docx
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_text(file_path):
    if file_path.endswith('.pdf'):
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text

    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""


def ai_response(query):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=query
            # messages=[{"role": "user", "content": query}]
        )
        return response.output[0].content[0].text
    
    except Exception as e:
        return f"AI Error: {str(e)}"
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Document, Chat
from .utils import extract_text, ai_response

# -------------------------------
# Upload Document
# -------------------------------
@api_view(['POST'])
def upload_document(request):
    file = request.FILES['file']
    doc = Document.objects.create(file=file)

    text = extract_text(doc.file.path)
    doc.extracted_text = text
    doc.save()

    return Response({"message": "File uploaded & processed"})


# -------------------------------
# Search in Knowledge Base
# -------------------------------
def search_answer(query):
    docs = Document.objects.all()
    query_words = query.lower().split()

    best_match = None
    max_score = 0

    for doc in docs:
        text = doc.extracted_text
        if not text:
            continue

        lines = text.split("\n")

        for i, line in enumerate(lines):
            clean_line = line.strip().lower()

            # Skip unwanted lines
            if (
                len(clean_line) < 20 or
                clean_line.endswith(":") or
                "overview" in clean_line or
                "knowledge base" in clean_line
            ):
                continue

            # Score matching
            score = sum(1 for word in query_words if word in clean_line)

            if score > max_score:
                max_score = score

                # अगर question line है → next line लो
                if clean_line.endswith("?") and i + 1 < len(lines):
                    best_match = lines[i + 1]
                else:
                    best_match = line

    return best_match if max_score > 0 else None        

# -------------------------------
#  Guided Flow
# -------------------------------
user_sessions = {}

def detect_insurance_type(message):
    msg = message.lower()

    if "health" in msg:
        return "health"
    elif "car" in msg or "vehicle" in msg:
        return "car"
    elif "life" in msg or "term" in msg:
        return "life"

    return None


def guided_flow(user_id, message):
    if user_id not in user_sessions:
        insurance_type = detect_insurance_type(message)

        if not insurance_type:
            return None

        user_sessions[user_id] = {
            "step": 1,
            "type": insurance_type
        }

        return f"Starting {insurance_type} insurance process. What is your name?"

    session = user_sessions[user_id]
    step = session["step"]
    insurance_type = session["type"]

    # ---------------- HEALTH ----------------
    if insurance_type == "health":

        if step == 1:
            session["name"] = message
            session["step"] = 2
            return "Who do you want to insure? (Self / Family / Parents)"

        elif step == 2:
            session["member"] = message
            session["step"] = 3
            return "What is the age of the eldest member?"

        elif step == 3:
            session["age"] = message
            session["step"] = 4
            return "What coverage amount do you need? (5L / 10L / 25L)"

        elif step == 4:
            session["coverage"] = message
            session["step"] = 5
            return "Any pre-existing medical condition? (Yes/No)"

        elif step == 5:
            session["medical"] = message

            # Recommendation Logic
            if "no" in message.lower():
                plan = "Basic Health Insurance Plan"
            else:
                plan = "Premium Health Insurance Plan with Critical Illness Cover"

            del user_sessions[user_id]
            return f"Recommended: {plan}"

    # ---------------- CAR ----------------
    elif insurance_type == "car":

        if step == 1:
            session["name"] = message
            session["step"] = 2
            return "Do you need new insurance or renewal?"

        elif step == 2:
            session["requirement"] = message
            session["step"] = 3
            return "Enter vehicle details (Brand/Model/Year)"

        elif step == 3:
            session["vehicle"] = message
            session["step"] = 4
            return "Do you want Comprehensive or Third Party plan?"

        elif step == 4:
            session["plan"] = message

            if "comprehensive" in message.lower():
                plan = "Comprehensive Car Insurance with Add-ons"
            else:
                plan = "Basic Third Party Insurance"

            del user_sessions[user_id]
            return f"Recommended: {plan}"

    # ---------------- LIFE ----------------
    elif insurance_type == "life":

        if step == 1:
            session["name"] = message
            session["step"] = 2
            return "What is your age?"

        elif step == 2:
            session["age"] = message
            session["step"] = 3
            return "What is your annual income?"

        elif step == 3:
            session["income"] = message
            session["step"] = 4
            return "What coverage do you need? (50L / 1Cr / 2Cr)"

        elif step == 4:
            session["coverage"] = message

            if "cr" in message.lower():
                plan = "High Value Term Insurance Plan"
            else:
                plan = "Standard Term Insurance Plan"

            del user_sessions[user_id]
            return f"Recommended: {plan}"

    return None
# -------------------------------
# Chat API
# -------------------------------
@api_view(['POST'])
def chat(request):
    user_msg = request.data.get("message")
    user_id = request.data.get("user_id", "default")

    if not user_msg:
        return Response({"error": "Message required"}, status=400)

    # Guided flow first
    guided_response = guided_flow(user_id, user_msg)

    if guided_response:
        return Response({"response": guided_response})

    # Knowledge base search
    response = search_answer(user_msg)

    if not response:
        response = ai_response(user_msg)

    return Response({"response": response})
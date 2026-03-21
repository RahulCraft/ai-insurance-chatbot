<<<<<<< HEAD
📌 Project Title
- AI Insurance Chatbot using Django REST Framework

📖 Overview

This project is an AI-powered insurance chatbot that answers user queries based on a knowledge base created from uploaded documents and provides guided insurance recommendations.

⚙️ Features
- Upload documents (PDF, DOCX)
- Extract and store text
- Answer queries from knowledge base
- AI fallback (OpenAI)
- Guided insurance chatbot (Health, Car, Life)
- Recommendation system

🏗️ Architecture
User → API (Django REST)
        ↓
Chatbot Logic
        ↓
Knowledge Base (DB)
        ↓
AI Fallback (OpenAI)


🧠 How Chatbot Retrieves Answers

1. User sends query
2. System searches extracted text in database
3. Uses keyword scoring to find best match
4. If found → returns knowledge-based answer
5. Else → fallback to OpenAI

🗄️ Database Schema
Document Table
-id
-file
-extracted_text

Chat Table
-id
-user_message
-bot_response
-created_at

User Session (In-memory)
-user_id
-step
-user data (age, income, etc.)

🤖 Guided Flow
-Health Insurance
-Car Insurance
-Term Life Insurance

Bot asks:
-Name
-Age
-Coverage
-Requirements

Then suggests best plan.
=======
📌 Project Title

AI Insurance Chatbot using Django REST Framework

📖 Overview

This project is an AI-powered insurance chatbot that answers user queries based on a knowledge base created from uploaded documents and provides guided insurance recommendations.


⚙️ Features

Upload documents (PDF, DOCX)

Extract and store text

Answer queries from knowledge base

AI fallback (OpenAI)

Guided insurance chatbot (Health, Car, Life)

Recommendation system


🏗️ Architecture
User → API (Django REST)
        ↓
Chatbot Logic
        ↓
Knowledge Base (DB)
        ↓
AI Fallback (OpenAI)


🧠 How Chatbot Retrieves Answers

1. User sends query

2. System searches extracted text in database

3. Uses keyword scoring to find best match

4. If found → returns knowledge-based answer

5. Else → fallback to OpenAI



🗄️ Database Schema
Document Table

id

file

extracted_text

Chat Table

id

user_message

bot_response

created_at

User Session (In-memory)

user_id

step

user data (age, income, etc.)



🤖 Guided Flow

Health Insurance

Car Insurance

Term Life Insurance

Bot asks:

Name

Age

Coverage

Requirements

Then suggests best plan.
>>>>>>> e522c86 (Intregrated UI for chatbor)

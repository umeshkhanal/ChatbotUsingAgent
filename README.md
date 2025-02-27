# Chatbot - CODEGURU

## Overview
This project is a **Django-based AI chatbot** named **CODEGURU - Your Technical Mentor** that leverages **Google Generative AI (Gemini Pro)** and **LangChain** to provide responses to user queries. The chatbot is capable of generating code, providing step-by-step instructions, refining problem statements, and offering project management guidance.

## Features
✅ **Conversational AI Chatbot** using Google Gemini Pro
✅ **Code Generation** for various programming languages
✅ **Step-by-Step Task Instructions** for problem-solving
✅ **Project Timeline Builder** for planning
✅ **Skill & Resource Recommendations** for learning
✅ **Code Review** with optimization suggestions
✅ **Tool Recommendations** for different tasks
✅ **Memory Storage** for context retention

## Technologies Used
- **Django** (Backend Framework)
- **LangChain** (AI Model Integration)
- **Google Generative AI (Gemini Pro)** (LLM Model)
- **SQLite** (Database for user management)
- **JSON & REST API** (For communication)

## Installation & Setup
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/umeshkhanal/ChatbotUsingAgent.git
cd SpeechEmotionRecognitionApp
```

### 2️⃣ Create & Activate Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
# Activate on Windows
venv\Scripts\activate
# Activate on macOS/Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a **.env** file and add your **Google API Key**:
```sh
GOOGLE_API_KEY=your-api-key-here
```
Or set it in your terminal:
```sh
export GOOGLE_API_KEY="your-api-key-here"
```

### 5️⃣ Run the Django Server
```sh
python manage.py runserver
```

## How It Works
1. **User sends a message** via frontend or API request.
2. **Django handles the request** and processes it through `chatbot_response()`.
3. **LangChain + Google Generative AI** generate responses.
4. **MemorySaver** retains context for improved conversations.
5. **Response is returned** as JSON for rendering in UI.


---
### Developed by Umesh Khanal 🚀


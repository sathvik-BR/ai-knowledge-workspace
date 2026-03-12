# AI Knowledge Workspace

AI Knowledge Workspace is an AI-powered web application that allows users to interact with PDF documents using natural language.
Users can upload documents, ask questions, perform semantic search, generate summaries, and create study flashcards using modern **Retrieval-Augmented Generation (RAG)** techniques.

---

## Live Demo

🚀 Try the application here:

https://ai-knowledge-workspace-2nm6jeycwgdgk3u92fzvnm.streamlit.app/

---

## Features

• Chat with PDF documents using AI
• Semantic search across document content
• Document summarization
• Automatic study flashcards generation
• Multi-PDF support
• Conversation history tracking
• Download AI generated chat, summaries, and flashcards
• Clean SaaS-style user interface

---

## Application Screenshots

### Chat Interface

![Chat Interface](Chat Interface.png)

### Semantic Search

![Semantic Search](Semantic Search.png)

### Document Summary

![Document Summary](doc summary.png)

### Study Flashcards

![Flashcards](study flashcard.png)

---

## How It Works

1. User uploads one or more PDF documents.
2. The system extracts text from the documents.
3. Text is split into smaller chunks for better processing.
4. Each chunk is converted into vector embeddings.
5. The embeddings are stored in a FAISS vector database.
6. When a user asks a question, relevant document chunks are retrieved.
7. The AI model generates answers using the retrieved context.

This process is known as **Retrieval-Augmented Generation (RAG)**.

---

## Technologies Used

Python
Streamlit
LangChain
FAISS Vector Database
HuggingFace Embeddings
Groq LLM API
Natural Language Processing (NLP)

---

## Installation

Clone the repository

```
git clone https://github.com/sathvik-BR/ai-knowledge-workspace.git
```

Navigate to the project directory

```
cd ai-knowledge-workspace
```

Install dependencies

```
pip install -r requirements.txt
```

Run the application

```
streamlit run app.py
```

---

## API Key Setup

This project uses the **Groq API** for AI responses.

Add your API key in Streamlit secrets or replace in code:

```
GROQ_API_KEY="your_api_key_here"
```

---

## Author

**B R Sathvik**
Artificial Intelligence and Machine Learning Student

LinkedIn
https://www.linkedin.com/in/b-r-sathvik-a9b785328

GitHub
https://github.com/sathvik-BR

---

## Project Purpose

This project was built to explore modern AI application development using:

• Retrieval-Augmented Generation
• Large Language Models
• Vector databases
• Document-based AI assistants

The goal is to create an intelligent workspace where users can easily understand and interact with large documents using AI.

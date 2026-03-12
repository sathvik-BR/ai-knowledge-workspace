# 🧠 AI Knowledge Workspace

AI Knowledge Workspace is an **AI-powered application that allows users to interact with PDF documents using natural language**.
Users can upload documents, ask questions, perform semantic search, generate summaries, and create study flashcards using **Retrieval-Augmented Generation (RAG)**.

---

## 🚀 Live Demo

Try the application here:

https://ai-knowledge-workspace-2nm6jeycwgdgk3u92fzvnm.streamlit.app/

---

## ✨ Features

• Chat with PDF documents using AI
• Semantic search across document content
• Automatic document summarization
• AI-powered study flashcards generation
• Multi-PDF support
• Conversation history tracking
• Download AI-generated chat responses
• Clean modern UI built with Streamlit

---

## 📷 Application Screenshots

### Chat Interface

<img src="chat-interface.png" width="900">

### Semantic Search

<img src="semantic-search.png" width="900">

### Document Summary

<img src="document-summary.png" width="900">

### Study Flashcards

<img src="study-flashcards.png" width="900">

---

## ⚙️ How It Works

1. Users upload one or more PDF documents.
2. The system extracts text from the documents.
3. Text is split into smaller chunks for efficient processing.
4. Each chunk is converted into vector embeddings.
5. The embeddings are stored in a **FAISS vector database**.
6. When a user asks a question, relevant chunks are retrieved.
7. The AI model generates responses using the retrieved context.

This approach is called **Retrieval-Augmented Generation (RAG)**.

---

## 🛠 Technologies Used

Python
Streamlit
LangChain
FAISS Vector Database
HuggingFace Embeddings
Groq LLM API
Natural Language Processing (NLP)

---

## 💻 Installation

Clone the repository

```bash
git clone https://github.com/sathvik-BR/ai-knowledge-workspace.git
```

Navigate to the project folder

```bash
cd ai-knowledge-workspace
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 🔑 API Key Setup

This project uses the **Groq API**.

Add your API key in **Streamlit Secrets**:

```
GROQ_API_KEY="your_api_key_here"
```

---

## 👨‍💻 Author

**B R Sathvik**
Artificial Intelligence and Machine Learning Student

GitHub
https://github.com/sathvik-BR

LinkedIn
https://www.linkedin.com/in/b-r-sathvik-a9b785328

---

## 🎯 Project Purpose

This project was built to explore **modern AI application development using RAG and LLMs**.
The goal is to create an intelligent workspace where users can easily understand and interact with large documents using AI.

import streamlit as st
import tempfile
import time
import base64

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from groq import Groq


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Knowledge Workspace",
    page_icon="🧠",
    layout="wide"
)


# ---------------- UI STYLE ----------------
st.markdown("""
<style>

.stApp {
background: linear-gradient(135deg,#0f172a,#1e293b,#020617);
color:white;
}

.chat-user{
background:#6366f1;
padding:10px;
border-radius:10px;
margin:8px 0;
}

.chat-ai{
background:#1e293b;
padding:10px;
border-radius:10px;
margin:8px 0;
}

.info-card{
background:#111827;
padding:15px;
border-radius:10px;
margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.title("⚙ Workspace")

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    st.divider()

    st.subheader("🕘 History")

    if "history" not in st.session_state:
        st.session_state.history = []

    for h in st.session_state.history[-10:]:

        if st.button(h):
            st.session_state.suggested_question = h


# ---------------- SESSION STORAGE ----------------
if "documents" not in st.session_state:
    st.session_state.documents = []

if uploaded_files:
    for file in uploaded_files:
        if file not in st.session_state.documents:
            st.session_state.documents.append(file)


# ---------------- TITLE ----------------
st.markdown(
"<h1 style='text-align:center'>🧠 AI Knowledge Workspace</h1>",
unsafe_allow_html=True
)

st.caption("AI-powered knowledge workspace for your documents")


# ---------------- VECTOR DATABASE ----------------
@st.cache_resource
def build_vector_db(files):

    all_docs = []

    for file in files:

        file.seek(0)

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            path = tmp.name

        loader = PyPDFLoader(path)
        docs = loader.load()

        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    split_docs = splitter.split_documents(all_docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.from_documents(split_docs, embeddings)

    return vector_db, split_docs, all_docs


vector_db = None
split_docs = []
all_docs = []

if st.session_state.documents:

    with st.spinner("Processing documents..."):

        vector_db, split_docs, all_docs = build_vector_db(
            st.session_state.documents
        )

        retriever = vector_db.as_retriever()


# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- NAVIGATION ----------------
tab1, tab2, tab3, tab4 = st.tabs(
["💬 Chat","🔎 Search","📚 Study","📄 Documents"]
)


# ================= CHAT TAB =================
with tab1:

    st.subheader("Chat With Documents")

    st.markdown("**Suggested Questions**")

    col1,col2,col3,col4 = st.columns(4)

    if col1.button("Summarize document"):
        st.session_state.suggested_question="Summarize this document"

    if col2.button("Key concepts"):
        st.session_state.suggested_question="What are the key concepts?"

    if col3.button("Explain main topic"):
        st.session_state.suggested_question="Explain the main topic"

    if col4.button("Generate flashcards"):
        st.session_state.suggested_question="Generate study flashcards"

    st.divider()


    for msg in st.session_state.messages:

        if msg["role"]=="user":
            st.markdown(
            f"<div class='chat-user'>🧑 {msg['content']}</div>",
            unsafe_allow_html=True
            )

        else:
            st.markdown(
            f"<div class='chat-ai'>🤖 {msg['content']}</div>",
            unsafe_allow_html=True
            )


    question = st.chat_input("Ask something about the documents")

    if "suggested_question" in st.session_state:
        question = st.session_state.suggested_question
        del st.session_state["suggested_question"]


    if question and vector_db:

        st.session_state.history.append(question)

        st.session_state.messages.append({
            "role":"user",
            "content":question
        })

        docs = retriever.invoke(question)

        context=""
        sources=[]

        for d in docs:

            context += d.page_content + "\n"
            sources.append(
            f"page {d.metadata.get('page',0)}"
            )

        prompt=f"""
Answer using ONLY this document context.

Context:
{context}

Question:
{question}
"""

        client = Groq(api_key="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")

        response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[{"role":"user","content":prompt}]
        )

        answer=response.choices[0].message.content

        stream=""
        placeholder=st.empty()

        for char in answer:

            stream+=char
            placeholder.markdown(stream)
            time.sleep(0.01)

        st.session_state.messages.append({
        "role":"assistant",
        "content":answer
        })

        st.markdown("### Sources")

        for s in set(sources):
            st.markdown(f"- {s}")

        st.rerun()


    # -------- DOWNLOAD CHAT --------
    if st.session_state.messages:

        chat_text=""

        for m in st.session_state.messages:

            role=m["role"]
            content=m["content"]

            chat_text+=f"{role}: {content}\n\n"

        st.download_button(
            "Download Chat",
            chat_text,
            file_name="chat_history.txt"
        )


# ================= SEARCH TAB =================
with tab2:

    st.subheader("Semantic Search")

    query=st.text_input("Search documents")

    if query and vector_db:

        results=retriever.invoke(query)

        for r in results:

            st.markdown(
            f"page {r.metadata.get('page',0)}"
            )

            st.write(r.page_content[:300])


# ================= STUDY TAB =================
with tab3:

    st.subheader("Generate Study Flashcards")

    if st.button("Generate Flashcards") and vector_db:

        context=" ".join([doc.page_content for doc in split_docs[:10]])

        prompt=f"Create study flashcards from:\n{context}"

        client = Groq(api_key="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")

        response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[{"role":"user","content":prompt}]
        )

        flashcards=response.choices[0].message.content

        st.write(flashcards)

        st.download_button(
            "Download Flashcards",
            flashcards,
            file_name="flashcards.txt"
        )


# ================= DOCUMENT TAB =================
with tab4:

    st.subheader("Document Info")

    if st.session_state.documents:

        doc = st.session_state.documents[0]

        doc.seek(0)

        b64 = base64.b64encode(doc.read()).decode()

        href = f'<a href="data:application/pdf;base64,{b64}" target="_blank">📄 Open PDF</a>'

        st.markdown(href, unsafe_allow_html=True)

    st.divider()

    st.markdown("<div class='info-card'>", unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    col1.metric("Documents",len(st.session_state.documents))
    col2.metric("Pages",len(all_docs))
    col3.metric("Chunks",len(split_docs) if st.session_state.documents else 0)

    st.markdown("</div>", unsafe_allow_html=True)


    if st.button("Summarize Documents") and vector_db:

        context=" ".join([doc.page_content for doc in split_docs[:20]])

        prompt=f"Summarize this content:\n{context}"

        client = Groq(api_key="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")

        response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[{"role":"user","content":prompt}]
        )

        summary=response.choices[0].message.content

        st.subheader("Document Summary")

        st.write(summary)

        st.download_button(
            "Download Summary",
            summary,
            file_name="summary.txt"
        )


# ---------------- FOOTER ----------------
st.markdown("---")

st.markdown("""

<center>

AI Knowledge Workspace  
© 2026 B R Sathvik  

<a href="https://github.com/sathvik-BR">GitHub</a> |
<a href="https://www.linkedin.com/in/b-r-sathvik-a9b785328">LinkedIn</a>

</center>

""",unsafe_allow_html=True)

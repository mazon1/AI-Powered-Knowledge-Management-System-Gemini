import streamlit as st
import PyPDF2
import google.generativeai as genai
import os

# Set up the API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', st.secrets.get("GOOGLE_API_KEY"))
genai.configure(api_key=GOOGLE_API_KEY)

# Set up the Streamlit interface
st.title("AI-Powered Knowledge Management System")
st.write("Upload PDF documents containing practitioner knowledge and ask tailored questions.")

# Process PDFs
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text

# Upload PDF
uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    documents = [extract_text_from_pdf(file) for file in uploaded_files]
    st.write("Extracted text from the uploaded PDFs.")
    
    # Input question from the researcher
    question = st.text_input("Enter your question:")

    # Function to process question and retrieve answer using Google Gemini
    def answer_question(question, documents):
        # Combine documents into a single context (this can be adjusted to improve results)
        context = " ".join(documents)

        # Use Google Gemini to generate an answer
        response = genai.generate_text(
            model="models/text-bison-001",
            prompt=f"Context: {context}\nQuestion: {question}"
        )

        return response.result

    if st.button("Get Answer"):
        if question and documents:
            response = answer_question(question, documents)
            st.write("Answer:", response)
        else:
            st.write("Please upload documents and enter a question.")

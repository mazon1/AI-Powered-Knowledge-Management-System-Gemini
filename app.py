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

# Function to split PDF into smaller chunks
def split_pdf(file, max_pages=10):
    pdf_reader = PyPDF2.PdfReader(file)
    chunks = []
    for i in range(0, len(pdf_reader.pages), max_pages):
        text = ""
        for page in range(i, min(i + max_pages, len(pdf_reader.pages))):
            text += pdf_reader.pages[page].extract_text()
        chunks.append(text)
    return chunks

# Upload PDF
uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    documents = []
    for file in uploaded_files:
        chunks = split_pdf(file)  # Split the PDF into smaller chunks
        documents.extend(chunks)  # Add each chunk to the documents list

    st.write("Extracted text from the uploaded PDFs.")

    # Input question from the researcher
    question = st.text_input("Enter your question:")

    # Function to process question and retrieve answer using Google Gemini
    def answer_question(question, documents):
        responses = []
        for doc in documents:
            try:
                # Use Google Gemini to generate an answer for each chunk
                response = genai.generate_text(
                    model="models/text-bison-001",
                    prompt=f"Context: {doc}\nQuestion: {question}"
                )
                responses.append(response.result)
            except Exception as e:
                st.error(f"Error generating response for a chunk: {e}")
                responses.append("[Error in generating response]")

        # Combine all the responses safely
        full_response = " ".join([resp for resp in responses if resp])  # Avoid joining empty strings or errors
        return full_response

    if st.button("Get Answer"):
        if question and documents:
            response = answer_question(question, documents)
            st.write("Answer:", response)
        else:
            st.write("Please upload documents and enter a question.")

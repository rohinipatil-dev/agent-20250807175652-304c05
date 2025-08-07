import streamlit as st
from openai import OpenAI
import PyPDF2

# Initialize OpenAI client
client = OpenAI()

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_response(pdf_text, user_question):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Here is some information extracted from a PDF: {pdf_text}"},
        {"role": "user", "content": f"Based on the above information, answer the following question: {user_question}"}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

def main():
    st.title("PDF Question Answering Agent")
    st.write("Upload a PDF file and ask questions based on its content.")

    pdf_file = st.file_uploader("Upload PDF", type="pdf")
    if pdf_file is not None:
        pdf_text = extract_text_from_pdf(pdf_file)
        st.text_area("Extracted Text", pdf_text, height=200)

        user_question = st.text_input("Ask a question about the PDF content:")
        if user_question:
            response = generate_response(pdf_text, user_question)
            st.write("Answer:", response)

if __name__ == "__main__":
    main()
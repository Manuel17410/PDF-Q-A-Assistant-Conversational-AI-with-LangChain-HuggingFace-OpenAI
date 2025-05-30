import os
import sys
import time
import streamlit as st
import speech_recognition as sr
from PyPDF2 import PdfReader
from fpdf import FPDF
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
import torch
import torchvision
from langchain.chat_models import ChatOpenAI

# Disable GPU usage
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Add template path
sys.path.append("c:/Users/manue/Desktop/DataScience/PDF/pdf")
from templates import css, bot_template, user_template


class PDFChatAssistant:
    def __init__(self):
        load_dotenv()
        st.set_page_config(page_title="PDF Q&A Assistant", page_icon=":books:", layout="wide")
        st.markdown(css, unsafe_allow_html=True)
        st.title("📄 Chat & Extract Insights from PDFs")

        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = None

    def get_pdf_text(self, pdf):
        reader = PdfReader(pdf)
        return "".join([page.extract_text() for page in reader.pages])

    def get_text_chunks(self, text):
        splitter = CharacterTextSplitter(separator="\n", chunk_size=4000, chunk_overlap=1000)
        return splitter.split_text(text)

    def get_vectorstore(self, chunks):
        embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
        return FAISS.from_texts(chunks, embedding)

    def get_conversation_chain(self, vectorstore):
        llm = ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo")
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        return ConversationalRetrievalChain.from_llm(llm, retriever=vectorstore.as_retriever(), memory=memory)

    def handle_userinput(self, question):
        typing_placeholder = st.empty()
        typing_placeholder.write('<div class="chat-message bot"><div class="message">Typing...</div></div>', unsafe_allow_html=True)
        time.sleep(1)

        response = st.session_state.conversation({'question': question})
        st.session_state.chat_history = response['chat_history']
        typing_placeholder.empty()

        for i, message in enumerate(st.session_state.chat_history):
            template = user_template if i % 2 == 0 else bot_template
            st.write(template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

    def listen_for_question(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("🎤 Listening...")
            audio = r.listen(source)
            try:
                question = r.recognize_google(audio)
                st.write(f"Your question: {question}")
                return question
            except sr.UnknownValueError:
                st.write("Sorry, I could not understand your question.")
            except sr.RequestError:
                st.write("Sorry, I'm having trouble accessing the speech recognition service.")
        return ""

    def export_chat_to_text(self):
        chat_text = "\n".join([message.content for message in st.session_state.chat_history])
        with open("chat_log.txt", "w") as f:
            f.write(chat_text)
        st.download_button("Download Chat as Text", "chat_log.txt")

    def export_chat_to_pdf(self):
        chat_pdf = FPDF()
        chat_pdf.add_page()
        chat_pdf.set_font("Arial", size=12)

        for message in st.session_state.chat_history:
            chat_pdf.multi_cell(0, 10, message.content.encode('latin-1', 'replace').decode('latin-1'))

        output_file = "chat_log.pdf"
        chat_pdf.output(output_file)
        st.download_button("Download Chat as PDF", output_file)

    def run(self):
        # Sidebar for PDF upload
        with st.sidebar:
            st.header("📂 Upload Your PDFs")
            pdf_docs = st.file_uploader("Select PDFs", accept_multiple_files=True)
            selected_pdf = None

            if pdf_docs:
                st.write(f"Number of PDFs uploaded: {len(pdf_docs)}")
                pdf_names = [pdf.name for pdf in pdf_docs]
                selected_name = st.selectbox("Select a PDF to analyze:", pdf_names)

                for pdf in pdf_docs:
                    if pdf.name == selected_name:
                        selected_pdf = pdf
                        break

                if selected_pdf:
                    reader = PdfReader(selected_pdf)
                    first_page_text = reader.pages[0].extract_text()
                    st.text_area("First Page Preview:", first_page_text[:500], height=100)

            if st.button("🔍 Analyze") and selected_pdf:
                with st.spinner("Analyzing..."):
                    raw_text = self.get_pdf_text(selected_pdf)
                    chunks = self.get_text_chunks(raw_text)
                    vectorstore = self.get_vectorstore(chunks)
                    st.session_state.conversation = self.get_conversation_chain(vectorstore)

        # Input handling
        question = ""
        #if st.button("🎤 Ask with Voice"):
            #question = self.listen_for_question()
        #else:
        question = st.text_input("💬 Ask about your PDFs:", placeholder="Type your question here...")

        if question:
            self.handle_userinput(question)

        if st.session_state.chat_history:
            st.header("💾 Export Chat")
            self.export_chat_to_text()
            self.export_chat_to_pdf()


def main():
    app = PDFChatAssistant()
    app.run()


if __name__ == "__main__":
    main()



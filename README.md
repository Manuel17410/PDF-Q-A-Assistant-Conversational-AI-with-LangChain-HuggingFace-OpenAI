# PDF Q&A Assistant: Conversational AI with LangChain, HuggingFace & OpenAI

https://pdf-reader-nwtsrtag8cax6jrc73ddpw.streamlit.app/

Web application that uses advanced language models (GPT-3.5-turbo) to enable interactive question-answering and insight extraction from uploaded PDF documents. Users can upload multiple PDFs, select one to analyze, and ask questions via text or voice input. The app processes the PDF content using embeddings and vector search to provide relevant, conversational answers. For enhanced usability, chat history can be exported as text or PDF files. This tool streamlines the process of extracting and interacting with information hidden in complex documents.

## Video Demonstration of the App on YouTube

To give you a quick overview of how the app works, I’ve created a demonstration video. While setting up the app locally can take a few minutes and sometimes lead to dependency issues, this video allows you to experience the website without any setup.

[![Watch the Demo](https://img.youtube.com/vi/R_fUTYp4lJ8/0.jpg)](https://www.youtube.com/watch?v=R_fUTYp4lJ8)

Additionally, I am actively working on hosting the app on a cloud platform to make it even easier to access.

## Logic of the App (Backend explanation)

The application works through the following steps to generate answers the questions:

1. **PDF Upload**: The app reads multiple PDF files and extracts the text content from them.

2. **Text Segmentation**: The extracted text is broken down into smaller, manageable sections for efficient processing.

3. **Language Model**: A language model is used to create vector representations (embeddings) of the text segments.

4. **Similarity Matching**: When you ask a question, the app compares it to the text segments and finds the ones most semantically similar.

5. **Answer Generation**: The relevant text chunks are passed to the language model, which formulates a response based on the extracted information from the PDFs.

## Frontend

It is possible to:

- Upload multiple PDF files
- Select a specific PDF for targeted questions
- Review the first page of any PDF
- Ask questions by typing or speaking
- Export the answers in either text or PDF format

![Example Image](images/ChatbotFrontend.png)

## Installation and Use

1- Copy the repository to your local machine by cloning it.

2- Install the necessary dependencies by executing this command: pip install -r requirements.txt

3- Get an HuggingFace key from HuggingFace and add it to the .env_secret file in the project directory: (change the name of the file to .env otherwise it will not work)

HUGGINGFACEHUB_API_TOKEN= your_API

4- Run the app using this command : streamlit run app.py

5- The app will open in the browser, and then upload documents and ask questions about it.









# PDF Q&A Assistant: Conversational AI with LangChain, HuggingFace & OpenAI

Web application that uses advanced language models (GPT-3.5-turbo) to enable interactive question-answering and insight extraction from uploaded PDF documents. Users can upload multiple PDFs, select one to analyze, and ask questions via text or voice input. The app processes the PDF content using embeddings and vector search to provide relevant, conversational answers. For enhanced usability, chat history can be exported as text or PDF files. This tool streamlines the process of extracting and interacting with information hidden in complex documents.


Sometimes after clicking the link below, you may get a "Zzzz , This app has gone to sleep due to inactivity. Would you like to wake it back up?" , then just click "Yes, get this back app" and it will load. It could take a few seconds.
Link to the app: https://pdf-q-a-assistant-clone-aodkhflaxqdgqe4bxj8jjr.streamlit.app/

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








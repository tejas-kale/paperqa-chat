from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API Key
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

vector_store = None

@app.route('/api/v1/upload', methods=['POST'])
def upload():
    global vector_store
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filepath = os.path.join("/tmp", file.filename)
        file.save(filepath)
        try:
            loader = PyPDFLoader(filepath)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(documents)
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            vector_store = FAISS.from_documents(docs, embeddings)
            return jsonify({"message": "File uploaded and processed successfully."})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/api/v1/query', methods=['POST'])
def query():
    global vector_store
    if vector_store is None:
        return jsonify({"error": "Please upload a document first."}), 400
    
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Question not provided."}), 400
    
    question = data['question']
    try:
        docs = vector_store.similarity_search(question)
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        chain = load_qa_chain(llm, chain_type="stuff")
        answer = chain.run(input_documents=docs, question=question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

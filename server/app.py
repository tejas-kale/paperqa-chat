from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from paperqa import Docs

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API Key
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

docs = Docs()

@app.route('/api/v1/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filepath = os.path.join("/tmp", file.filename)
        file.save(filepath)
        try:
            docs.add(filepath)
            return jsonify({"message": "File uploaded and processed successfully."})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/api/v1/query', methods=['POST'])
def query():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Question not provided."}), 400
    
    question = data['question']
    try:
        answer = docs.query(question)
        return jsonify({"answer": answer.answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

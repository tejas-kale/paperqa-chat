from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/v1/query', methods=['POST'])
def query():
    # Placeholder for PaperQA logic
    return jsonify({"answer": "This is a placeholder answer."})

if __name__ == '__main__':
    app.run(debug=True)

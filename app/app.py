from flask import Flask, request, jsonify
import os
from paperqa import Docs, Answer

app = Flask(__name__)

# Store indexed projects in memory for demo purposes
indexed_projects = {}


@app.route("/index", methods=["POST"])
def index_papers():
    data = request.get_json()
    dir_path = data.get("dir_path")
    if not dir_path or not os.path.isdir(dir_path):
        return jsonify({"error": "Invalid directory path."}), 400
    docs = Docs()
    for fname in os.listdir(dir_path):
        fpath = os.path.join(dir_path, fname)
        if os.path.isfile(fpath):
            docs.add(fpath)
    indexed_projects[dir_path] = docs
    return jsonify({"message": f"Indexed {len(docs.docs)} documents from {dir_path}."})


@app.route("/ask", methods=["POST"])
def ask_paper_qa():
    data = request.get_json()
    dir_path = data.get("project")
    question = data.get("question")
    if not dir_path or not question:
        return jsonify({"error": "Project and question are required."}), 400
    docs = indexed_projects.get(dir_path)
    if not docs:
        return jsonify({"error": "Project not indexed. Please index first."}), 404
    answer: Answer = docs.query(question)
    return jsonify(
        {"answer": answer.answer, "references": [ref.ref for ref in answer.references]}
    )


if __name__ == "__main__":
    app.run(debug=True)

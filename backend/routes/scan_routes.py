
# routes/scan_routes.py - Document Scanning Routes
import os
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db
from models.document import Document
from flask_cors import CORS  # ✅ Import CORS
from utils.similarity import compute_tfidf_similarity, compute_ai_similarity
import PyPDF2
import asyncio 

scan_bp = Blueprint('scan', __name__)
CORS(scan_bp, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt","pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 5MB
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path):
    try:
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif file_path.endswith('.pdf'):
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return " ".join(filter(None,[page.extract_text() for page in reader.pages if page.extract_text()]))
        else:
            return None
    except Exception as e:
        return None

@scan_bp.route('/', methods=['POST'])
@login_required
def scan_document():
    if current_user.credits <= 0:
        return jsonify({"error": "Not enough credits"}), 403

    current_user.credits -= 1
    db.session.commit()
    
    return jsonify({"message": "Document scanned successfully, 1 credit deducted"}), 200

@scan_bp.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    #file = request.files['file']
    file = request.files.get("file")
    user_id = request.headers.get("user_id")  # Get user_id from headers

    if not file or not user_id:
        return jsonify({"error": "File and user_id are required"}), 400

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset pointer

    if file_size > MAX_FILE_SIZE:
        return jsonify({"error": "File too large. Max size is 5MB."}), 400


    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
            
    # try:
    #     content = extract_text_from_file(file_path)
    #     if content is None:
    #         return jsonify({"error": "Unsupported file format"}), 400
        
    # except UnicodeDecodeError:
    #     return jsonify({"error": "Unsupported file type. Only text files are allowed."}), 400
    

    #user_id = request.headers.get('user_id')  # Get user_id from request headers

    # if not user_id:
    #     return jsonify({"error": "User ID is required"}), 400
    document_text = extract_text_from_file(file_path)
    # Save document to DB

    if not document_text:
        return jsonify({"error": "Unsupported file format or empty content"}), 400
    print("Computing TF-IDF for document:", document_text[:500])  # Print first 500 chars

    new_doc = Document(user_id=int(user_id), filename=filename, content=document_text)
    try:
        db.session.add(new_doc)
        db.session.commit()
        return jsonify({
        "filename": filename,
        "message": "File uploaded successfully",
        "document_text": document_text  # ✅ Return extracted text
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify({"message": "File uploaded successfully", "filename": filename}), 201

    # data = request.json
    # new_doc = Document(user_id=data['user_id'], filename=data['filename'], content=data['content'])
    # db.session.add(new_doc)
    # db.session.commit()
    # return jsonify({'message': 'Document uploaded successfully'})

@scan_bp.route('/match', methods=['POST'])
async def match_documents():
    """
    Match uploaded document against stored documents.
    """
    data = request.json
    print("Received request data:", data)
    new_doc = data.get("document_text")

    if not new_doc:
        return jsonify({"error": "No document text provided"}), 400
    print(Document.query.all())  # Check if documents exist

    documents = Document.query.all()
    if not documents:
        return jsonify({"error": "No stored documents available for comparison"}), 404
    
    stored_docs = [doc.content for doc in documents]
    stored_filenames = [doc.filename for doc in documents]

    # stored_docs = []
    # stored_filenames = []

    # for doc in documents:
    #     stored_docs.append(doc.content)
    #     stored_filenames.append(doc.filename)

    try:
        print("⚡ Running TF-IDF Similarity")
        tfidf_scores = compute_tfidf_similarity(new_doc, stored_docs)
        print("✅ TF-IDF Scores:", tfidf_scores)

        print("⚡ Running AI Similarity")
        ai_scores = await compute_ai_similarity(new_doc, stored_docs)
        print("✅ AI Scores:", ai_scores)
    except Exception as e:
        print("❌ Error in similarity calculation:", str(e))  # Debug print
        return jsonify({"error": f"Similarity calculation failed: {str(e)}"}), 500

    # Combine results
    try:
        results = [
            {"filename": stored_filenames[i], "tfidf_score": float(tfidf_scores[i]), "ai_score": float(ai_scores[i])}
            for i in range(len(stored_docs))
        ]
        print("✅ Combined Results:", results)
        # Sort results by AI score
        results = sorted(results, key=lambda x: x["ai_score"], reverse=True)
        print("✅ Sorted Results:", results)
    except Exception as e:
        print("❌ Error in result processing:", str(e))  # Debug print
        return jsonify({"error": f"Result processing failed: {str(e)}"}), 500
    
    print("✅ Final Results:", results)
    return jsonify({"matches": results})
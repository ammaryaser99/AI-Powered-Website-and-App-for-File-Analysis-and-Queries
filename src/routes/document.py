import os
import uuid
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from src.models.user import db, User
from src.models.document import Document, DocumentChunk
from src.utils.document_processor import DocumentProcessor, EmbeddingService, VectorStore


document_bp = Blueprint('document', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

doc_processor = DocumentProcessor()
embedding_service = EmbeddingService()
vector_store = VectorStore()


@document_bp.route('/documents', methods=['GET'])
def list_documents():
    user_id = request.args.get('user_id', type=int)
    query = Document.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    documents = query.all()
    return jsonify({'documents': [d.to_dict() for d in documents]})


@document_bp.route('/documents/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    user_id = request.form.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    filename = secure_filename(file.filename)
    file_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_FOLDER, f"{file_id}_{filename}")
    file.save(save_path)

    file_size = os.path.getsize(save_path)
    file_type = os.path.splitext(filename)[1].lower()

    doc_record = Document(
        user_id=user_id,
        filename=filename,
        file_type=file_type,
        file_size=file_size,
        file_path=save_path,
        processing_status='processing'
    )
    db.session.add(doc_record)
    db.session.commit()

    # Process file
    result = doc_processor.process_document(save_path, filename)
    if not result.get('success'):
        doc_record.processing_status = 'failed'
        db.session.commit()
        return jsonify({'error': result.get('error', 'processing failed')}), 500

    doc_record.extracted_text = result['extracted_text']
    doc_record.processing_status = 'completed'
    doc_record.processing_completed_at = db.func.current_timestamp()
    db.session.commit()

    embeddings = embedding_service.generate_embeddings([c['text'] for c in result['chunks']])

    for idx, chunk in enumerate(result['chunks']):
        chunk_record = DocumentChunk(
            document_id=doc_record.id,
            chunk_text=chunk['text'],
            chunk_order=idx,
            page_number=chunk.get('page_number'),
            section_type=chunk.get('section_type')
        )
        db.session.add(chunk_record)
    db.session.commit()

    vector_store.add_chunks(doc_record.id, result['chunks'], embeddings)

    return jsonify({'document': doc_record.to_dict()})


@document_bp.route('/documents/<int:doc_id>/status', methods=['GET'])
def document_status(doc_id):
    doc = Document.query.get_or_404(doc_id)
    return jsonify({'status': doc.processing_status})


@document_bp.route('/documents/<int:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    vector_store.delete_document_chunks(doc.id)
    db.session.delete(doc)
    db.session.commit()
    return '', 204

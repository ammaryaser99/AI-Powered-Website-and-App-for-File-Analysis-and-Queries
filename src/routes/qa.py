from flask import Blueprint, request, jsonify

from src.models.user import db, User
from src.models.document import Document, Conversation
from src.utils.qa_service import QuestionAnsweringService

qa_bp = Blueprint('qa', __name__)
qa_service = QuestionAnsweringService()


@qa_bp.route('/qa/ask', methods=['POST'])
def ask_question():
    data = request.get_json() or {}
    question = data.get('question')
    document_id = data.get('document_id')
    user_id = data.get('user_id')

    if not question or not document_id or not user_id:
        return jsonify({'error': 'question, document_id and user_id are required'}), 400

    document = Document.query.get(document_id)
    if not document:
        return jsonify({'error': 'Document not found'}), 404

    result = qa_service.answer_question(question, document_id=document_id)

    conv = Conversation(
        user_id=user_id,
        document_id=document_id,
        question=question,
        answer=result['answer'],
        confidence_score=result.get('confidence_score'),
        sources_cited=str([s['chunk_id'] for s in result.get('sources', [])])
    )
    db.session.add(conv)
    db.session.commit()

    return jsonify(result)


@qa_bp.route('/qa/conversations', methods=['GET'])
def list_conversations():
    user_id = request.args.get('user_id', type=int)
    document_id = request.args.get('document_id', type=int)
    query = Conversation.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if document_id:
        query = query.filter_by(document_id=document_id)
    conversations = query.order_by(Conversation.timestamp.desc()).all()
    return jsonify({'conversations': [c.to_dict() for c in conversations]})

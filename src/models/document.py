from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # PDF, DOCX, XLSX
    file_size = db.Column(db.Integer, nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    upload_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    processing_status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    processing_completed_at = db.Column(db.DateTime)
    document_hash = db.Column(db.String(64))
    extracted_text = db.Column(db.Text)
    
    # Relationship with chunks
    chunks = db.relationship('DocumentChunk', backref='document', lazy=True, cascade='all, delete-orphan')
    conversations = db.relationship('Conversation', backref='document', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Document {self.filename}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'upload_timestamp': self.upload_timestamp.isoformat() if self.upload_timestamp else None,
            'processing_status': self.processing_status,
            'processing_completed_at': self.processing_completed_at.isoformat() if self.processing_completed_at else None,
            'document_hash': self.document_hash
        }

class DocumentChunk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    chunk_text = db.Column(db.Text, nullable=False)
    chunk_order = db.Column(db.Integer, nullable=False)
    page_number = db.Column(db.Integer)
    section_type = db.Column(db.String(50))  # paragraph, table, header, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<DocumentChunk {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'chunk_text': self.chunk_text,
            'chunk_order': self.chunk_order,
            'page_number': self.page_number,
            'section_type': self.section_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    confidence_score = db.Column(db.Float)
    sources_cited = db.Column(db.Text)  # JSON string of chunk IDs
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Conversation {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'document_id': self.document_id,
            'question': self.question,
            'answer': self.answer,
            'confidence_score': self.confidence_score,
            'sources_cited': self.sources_cited,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


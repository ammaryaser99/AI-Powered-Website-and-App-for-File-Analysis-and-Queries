# AI Document Processor

A powerful web application that uses artificial intelligence to read and understand your PDF, Word, and Excel documents, allowing you to ask questions about their content instead of manually searching through them.

## 🚀 Live Demo

**Frontend Application**: https://orlvwkrm.manus.space

## ✨ Features

### 📄 Document Processing
- **Multi-format Support**: Upload PDF, DOCX, and XLSX files
- **Intelligent Text Extraction**: Advanced parsing for different document types
- **Real-time Processing**: Live status updates during document processing
- **File Management**: Easy upload, view, and delete functionality

### 🤖 AI-Powered Question Answering
- **Natural Language Queries**: Ask questions in plain English
- **Context-Aware Responses**: AI understands document context
- **Confidence Scoring**: Get confidence levels for AI responses
- **Conversation History**: Track all your questions and answers

### 📱 Mobile-First Design
- **Responsive Interface**: Works perfectly on all devices
- **Touch Optimized**: Designed for mobile interaction
- **Voice Input**: Speak your questions on mobile devices
- **Progressive Web App**: Install on your device like a native app

### 🎨 Modern User Experience
- **Clean Interface**: Professional, intuitive design
- **Dark Mode Support**: Comfortable viewing in any lighting
- **Real-time Updates**: Live processing status and notifications
- **Accessibility**: Full keyboard navigation and screen reader support

## 🏗️ Architecture

### Backend (Flask API)
- **Document Processing**: PyMuPDF, python-docx, openpyxl
- **AI Engine**: Sentence Transformers for embeddings
- **Database**: SQLite with SQLAlchemy ORM
- **API**: RESTful endpoints with CORS support

### Frontend (React)
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS with shadcn/ui components
- **Icons**: Lucide React icons
- **State Management**: React hooks and context

## 📋 Requirements

- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 10GB available space

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-document-processor
```

### 2. Backend Setup
```bash
cd ai-document-processor
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

### 3. Frontend Setup
```bash
cd ai-document-frontend
npm install
npm run dev
```

### 4. Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

## 📚 API Documentation

### Document Endpoints
```
POST /api/documents/upload     - Upload a document
GET  /api/documents           - List user documents
GET  /api/documents/{id}/status - Check processing status
DELETE /api/documents/{id}    - Delete a document
```

### Question Answering Endpoints
```
POST /api/qa/ask              - Ask a question
GET  /api/qa/conversations    - Get conversation history
```

### Health Check
```
GET  /api/health              - API health status
```

## 🔧 Configuration

### Environment Variables
```bash
# Backend Configuration
DATABASE_URL=sqlite:///documents.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Frontend Configuration
VITE_API_BASE_URL=http://localhost:5000/api
```

## 📱 Mobile App Development

The application is designed with mobile-first principles and includes:

### Progressive Web App Features
- **Offline Support**: Cache documents for offline viewing
- **Push Notifications**: Get notified when processing completes
- **Home Screen Installation**: Add to device home screen

### Native App Development
For native mobile apps, consider:
- **React Native**: Reuse existing React components
- **Flutter**: High-performance cross-platform development
- **Native**: iOS (Swift) and Android (Kotlin) for maximum performance

## 🔒 Security Features

- **File Validation**: Strict file type and size checking
- **Input Sanitization**: Prevent injection attacks
- **CORS Protection**: Secure cross-origin requests
- **Error Handling**: Graceful error management

## 🚀 Deployment

### Production Build
```bash
# Frontend
cd ai-document-frontend
npm run build

# Backend
cd ai-document-processor
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

### Cloud Deployment
- **Heroku**: Easy deployment with buildpacks
- **AWS**: EC2, ECS, or Lambda
- **Google Cloud**: App Engine or Compute Engine
- **Azure**: App Service or Container Instances

## 🧪 Testing

### Backend Testing
```bash
cd ai-document-processor
python -m pytest tests/
```

### Frontend Testing
```bash
cd ai-document-frontend
npm test
```

## 📊 Performance

- **Document Processing**: ~2-5 seconds per document
- **Question Answering**: ~1-3 seconds per query
- **File Upload**: Supports up to 16MB files
- **Concurrent Users**: Scales with server resources

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Flask**: Web framework for Python
- **React**: JavaScript library for building user interfaces
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Beautiful UI components
- **Sentence Transformers**: State-of-the-art sentence embeddings
- **PyMuPDF**: PDF processing library
- **python-docx**: Word document processing
- **openpyxl**: Excel file processing

## 📞 Support

For questions, issues, or feature requests:
- Create an issue on GitHub
- Check the documentation
- Review the deployment guide

---

**Built with ❤️ using modern web technologies and AI**


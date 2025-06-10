# AI Document Processor - Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying and running the AI Document Processor system, which consists of a Flask backend API and a React frontend application.

## System Requirements

### Backend Requirements
- Python 3.11 or higher
- 4GB RAM minimum (8GB recommended)
- 10GB disk space
- Internet connection for AI model downloads

### Frontend Requirements
- Node.js 18 or higher
- npm or yarn package manager
- Modern web browser

## Quick Start

### 1. Backend Setup

```bash
# Navigate to the backend directory
cd ai-document-processor

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python src/main.py
```

The backend will be available at `http://localhost:5000`

### 2. Frontend Setup

```bash
# Navigate to the frontend directory
cd ai-document-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 3. Production Build

```bash
# Build for production
npm run build

# The built files will be in the 'dist' directory
```

## Backend API Endpoints

### Document Management
- `POST /api/documents/upload` - Upload a new document
- `GET /api/documents` - List all documents for a user
- `GET /api/documents/{id}/status` - Check document processing status
- `DELETE /api/documents/{id}` - Delete a document

### Question Answering
- `POST /api/qa/ask` - Ask a question about a document
- `GET /api/qa/conversations` - Get conversation history

### Health Check
- `GET /api/health` - Check API health status

## Configuration

### Backend Configuration

The Flask application can be configured through environment variables:

```bash
# Database configuration
DATABASE_URL=sqlite:///documents.db

# Upload configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB

# AI model configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Frontend Configuration

Update the API base URL in `src/App.jsx`:

```javascript
const API_BASE_URL = 'http://your-backend-url/api'
```

## Supported File Types

- **PDF**: Portable Document Format files
- **DOCX**: Microsoft Word documents
- **XLSX**: Microsoft Excel spreadsheets

## Features

### Core Functionality
- Document upload and processing
- AI-powered question answering
- Conversation history
- Real-time processing status
- File management (view, delete)

### Mobile Features
- Responsive design for all screen sizes
- Touch-optimized interface
- Voice input support (on supported browsers)
- Mobile-friendly navigation
- Progressive Web App capabilities

### AI Capabilities
- Text extraction from documents
- Semantic search and retrieval
- Context-aware question answering
- Confidence scoring
- Multi-document support

## Deployment Options

### Option 1: Local Development
Use the quick start instructions above for local development and testing.

### Option 2: Production Deployment
For production deployment, consider:

1. **Backend**: Deploy using Gunicorn with nginx
2. **Frontend**: Build and serve static files
3. **Database**: Use PostgreSQL for production
4. **Security**: Implement authentication and HTTPS

### Option 3: Cloud Deployment
The system can be deployed to various cloud platforms:
- **Heroku**: Easy deployment with buildpacks
- **AWS**: EC2, ECS, or Lambda deployment
- **Google Cloud**: App Engine or Compute Engine
- **Azure**: App Service or Container Instances

## Security Considerations

### Authentication
Implement user authentication for production use:
- JWT tokens for API authentication
- Session management
- User registration and login

### File Security
- Validate file types and sizes
- Scan uploads for malware
- Implement access controls
- Use secure file storage

### API Security
- Rate limiting
- CORS configuration
- Input validation
- SQL injection prevention

## Troubleshooting

### Common Issues

**Backend won't start:**
- Check Python version (3.11+ required)
- Verify all dependencies are installed
- Check port 5000 is available

**Frontend build fails:**
- Ensure Node.js 18+ is installed
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall

**Document processing fails:**
- Check file format is supported
- Verify file size is under 16MB
- Ensure sufficient disk space

**AI responses are poor:**
- Check document text extraction quality
- Verify embedding model is loaded
- Consider document preprocessing

### Performance Optimization

**Backend Performance:**
- Use production WSGI server (Gunicorn)
- Implement caching for processed documents
- Optimize database queries
- Use background task queues

**Frontend Performance:**
- Enable gzip compression
- Use CDN for static assets
- Implement lazy loading
- Optimize bundle size

## Monitoring and Logging

### Backend Logging
The Flask application logs to console by default. For production:
- Configure file-based logging
- Use structured logging (JSON)
- Implement log rotation
- Monitor error rates

### Frontend Monitoring
- Implement error tracking (Sentry)
- Monitor performance metrics
- Track user interactions
- Monitor API response times

## Backup and Recovery

### Database Backup
```bash
# SQLite backup
cp documents.db documents_backup.db

# PostgreSQL backup
pg_dump dbname > backup.sql
```

### File Backup
- Backup uploaded documents regularly
- Store backups in secure location
- Test restore procedures
- Implement automated backups

## Support and Maintenance

### Regular Maintenance
- Update dependencies regularly
- Monitor security vulnerabilities
- Review and rotate logs
- Performance monitoring

### Scaling Considerations
- Horizontal scaling with load balancers
- Database replication
- File storage scaling
- Caching strategies

## License and Credits

This AI Document Processor was built using:
- Flask (Backend framework)
- React (Frontend framework)
- PyMuPDF (PDF processing)
- python-docx (Word document processing)
- openpyxl (Excel processing)
- Sentence Transformers (AI embeddings)
- Tailwind CSS (Styling)
- shadcn/ui (UI components)

For support or questions, please refer to the documentation or contact the development team.


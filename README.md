# AI Document Processor

This project provides a simple proof-of-concept for analysing uploaded documents and asking questions about their content.  A Flask API performs document processing and question answering while a React frontend (not included here) communicates with the API.

## Features

- Upload PDF, DOCX and XLSX files
- Extract text content and split it into searchable chunks
- Store document chunks in a local ChromaDB instance
- Ask questions about a document and receive answers with basic confidence scores
- SQLite database using SQLAlchemy

## Project Structure

```
├── main.py               # Flask application entry
├── requirements.txt      # Python dependencies
├── src/
│   ├── models/
│   │   ├── document.py   # Document related models
│   │   └── user.py       # User model and DB instance
│   ├── routes/
│   │   ├── document.py   # Document API endpoints
│   │   ├── qa.py         # Question answering endpoints
│   │   └── user.py       # User management endpoints
│   └── utils/
│       ├── document_processor.py  # Text extraction and vector store helpers
│       └── qa_service.py          # Question answering service
```

## Running Locally

1. **Install dependencies**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Start the application**

```bash
python main.py
```

The API will be available at `http://localhost:5000/api`.

A simple placeholder page is served at `http://localhost:5000`.
Uploaded files are stored in the `src/uploads` directory and a SQLite database is created under `database/app.db` on first run.

## Notes

The React frontend referenced in the documentation is not part of this repository.  You can interact with the API using any HTTP client such as `curl` or Postman.

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet.jsx'
import { 
  Upload, 
  FileText, 
  MessageSquare, 
  Send, 
  Trash2, 
  Download,
  Brain,
  FileSpreadsheet,
  FileImage,
  Loader2,
  CheckCircle,
  XCircle,
  Clock,
  Menu,
  Smartphone,
  Camera,
  Mic,
  X
} from 'lucide-react'
import './App.css'

const API_BASE_URL = 'http://localhost:5000/api'

function App() {
  const [documents, setDocuments] = useState([])
  const [selectedDocument, setSelectedDocument] = useState(null)
  const [conversations, setConversations] = useState([])
  const [currentQuestion, setCurrentQuestion] = useState('')
  const [isUploading, setIsUploading] = useState(false)
  const [isAsking, setIsAsking] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [isMobile, setIsMobile] = useState(false)
  const [showDocuments, setShowDocuments] = useState(false)
  const [isListening, setIsListening] = useState(false)

  // Detect mobile device
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768)
    }
    
    checkMobile()
    window.addEventListener('resize', checkMobile)
    
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  // Fetch documents on component mount
  useEffect(() => {
    fetchDocuments()
  }, [])

  // Fetch conversations when document is selected
  useEffect(() => {
    if (selectedDocument) {
      fetchConversations(selectedDocument.id)
    }
  }, [selectedDocument])

  const fetchDocuments = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/documents?user_id=1`)
      const data = await response.json()
      setDocuments(data.documents || [])
    } catch (error) {
      console.error('Error fetching documents:', error)
    }
  }

  const fetchConversations = async (documentId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/qa/conversations?user_id=1&document_id=${documentId}`)
      const data = await response.json()
      setConversations(data.conversations || [])
    } catch (error) {
      console.error('Error fetching conversations:', error)
    }
  }

  const handleFileUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    setIsUploading(true)
    setUploadProgress(0)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('user_id', '1')

    try {
      // Simulate progress for better UX
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 10, 90))
      }, 200)

      const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: 'POST',
        body: formData
      })

      clearInterval(progressInterval)
      setUploadProgress(100)

      const data = await response.json()
      
      if (response.ok) {
        await fetchDocuments()
        // Auto-select the uploaded document
        setSelectedDocument(data.document)
        // Close mobile sheet if open
        if (isMobile) {
          setShowDocuments(false)
        }
      } else {
        alert(data.error || 'Upload failed')
      }
    } catch (error) {
      console.error('Error uploading file:', error)
      alert('Upload failed')
    } finally {
      setIsUploading(false)
      setUploadProgress(0)
      // Reset file input
      event.target.value = ''
    }
  }

  const handleAskQuestion = async () => {
    if (!currentQuestion.trim() || !selectedDocument) return

    setIsAsking(true)

    try {
      const response = await fetch(`${API_BASE_URL}/qa/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question: currentQuestion,
          document_id: selectedDocument.id,
          user_id: 1
        })
      })

      const data = await response.json()
      
      if (response.ok) {
        // Add the new conversation to the list
        setConversations(prev => [data, ...prev])
        setCurrentQuestion('')
      } else {
        alert(data.error || 'Failed to get answer')
      }
    } catch (error) {
      console.error('Error asking question:', error)
      alert('Failed to get answer')
    } finally {
      setIsAsking(false)
    }
  }

  const handleDeleteDocument = async (documentId) => {
    if (!confirm('Are you sure you want to delete this document?')) return

    try {
      const response = await fetch(`${API_BASE_URL}/documents/${documentId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        await fetchDocuments()
        if (selectedDocument && selectedDocument.id === documentId) {
          setSelectedDocument(null)
          setConversations([])
        }
      } else {
        alert('Failed to delete document')
      }
    } catch (error) {
      console.error('Error deleting document:', error)
      alert('Failed to delete document')
    }
  }

  // Voice input functionality (mock implementation)
  const handleVoiceInput = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
      const recognition = new SpeechRecognition()
      
      recognition.continuous = false
      recognition.interimResults = false
      recognition.lang = 'en-US'
      
      recognition.onstart = () => {
        setIsListening(true)
      }
      
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript
        setCurrentQuestion(transcript)
        setIsListening(false)
      }
      
      recognition.onerror = () => {
        setIsListening(false)
        alert('Voice recognition failed. Please try again.')
      }
      
      recognition.onend = () => {
        setIsListening(false)
      }
      
      recognition.start()
    } else {
      alert('Voice recognition is not supported in this browser.')
    }
  }

  const getFileIcon = (fileType) => {
    switch (fileType.toLowerCase()) {
      case 'pdf':
        return <FileText className="h-5 w-5 text-red-500" />
      case 'docx':
        return <FileText className="h-5 w-5 text-blue-500" />
      case 'xlsx':
        return <FileSpreadsheet className="h-5 w-5 text-green-500" />
      default:
        return <FileImage className="h-5 w-5 text-gray-500" />
    }
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return <Badge variant="default" className="bg-green-500"><CheckCircle className="h-3 w-3 mr-1" />Ready</Badge>
      case 'processing':
        return <Badge variant="secondary"><Loader2 className="h-3 w-3 mr-1 animate-spin" />Processing</Badge>
      case 'failed':
        return <Badge variant="destructive"><XCircle className="h-3 w-3 mr-1" />Failed</Badge>
      default:
        return <Badge variant="outline"><Clock className="h-3 w-3 mr-1" />Pending</Badge>
    }
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  // Document panel component for reuse
  const DocumentPanel = () => (
    <Card className="h-full">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Upload className="h-5 w-5" />
          <span>Documents</span>
          {isMobile && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowDocuments(false)}
              className="ml-auto"
            >
              <X className="h-4 w-4" />
            </Button>
          )}
        </CardTitle>
        <CardDescription>
          Upload and manage your PDF, Word, and Excel files
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* File Upload */}
        <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
          <input
            type="file"
            accept=".pdf,.docx,.xlsx"
            onChange={handleFileUpload}
            disabled={isUploading}
            className="hidden"
            id="file-upload"
          />
          <label htmlFor="file-upload" className="cursor-pointer">
            <Upload className="h-8 w-8 mx-auto text-gray-400 mb-2" />
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {isUploading ? 'Uploading...' : 'Click to upload or drag and drop'}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              PDF, DOCX, XLSX up to 16MB
            </p>
          </label>
        </div>

        {/* Upload Progress */}
        {isUploading && (
          <div className="space-y-2">
            <Progress value={uploadProgress} className="w-full" />
            <p className="text-xs text-center text-gray-500">{uploadProgress}% uploaded</p>
          </div>
        )}

        <Separator />

        {/* Document List */}
        <ScrollArea className={isMobile ? "h-64" : "h-96"}>
          <div className="space-y-2">
            {documents.map((doc) => (
              <Card 
                key={doc.id} 
                className={`cursor-pointer transition-all hover:shadow-md ${
                  selectedDocument?.id === doc.id ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : ''
                }`}
                onClick={() => {
                  setSelectedDocument(doc)
                  if (isMobile) {
                    setShowDocuments(false)
                  }
                }}
              >
                <CardContent className="p-3">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-3 flex-1 min-w-0">
                      {getFileIcon(doc.file_type)}
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                          {doc.filename}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                          {formatFileSize(doc.file_size)}
                        </p>
                        <div className="mt-1">
                          {getStatusBadge(doc.processing_status)}
                        </div>
                      </div>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation()
                        handleDeleteDocument(doc.id)
                      }}
                      className="text-red-500 hover:text-red-700 hover:bg-red-50"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
            {documents.length === 0 && (
              <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                <FileText className="h-12 w-12 mx-auto mb-2 opacity-50" />
                <p>No documents uploaded yet</p>
              </div>
            )}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Brain className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className={`${isMobile ? 'text-xl' : 'text-2xl'} font-bold text-gray-900 dark:text-white`}>
                  AI Document Processor
                </h1>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {isMobile ? 'Ask questions about files' : 'Ask questions about your documents'}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              {isMobile && (
                <Sheet open={showDocuments} onOpenChange={setShowDocuments}>
                  <SheetTrigger asChild>
                    <Button variant="outline" size="sm">
                      <Menu className="h-4 w-4 mr-2" />
                      Documents
                    </Button>
                  </SheetTrigger>
                  <SheetContent side="left" className="w-80">
                    <DocumentPanel />
                  </SheetContent>
                </Sheet>
              )}
              <Badge variant="outline" className="text-xs">
                <Smartphone className="h-3 w-3 mr-1" />
                {documents.length} doc{documents.length !== 1 ? 's' : ''}
              </Badge>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className={`grid ${isMobile ? 'grid-cols-1' : 'grid-cols-1 lg:grid-cols-3'} gap-8`}>
          {/* Document Management Panel - Desktop Only */}
          {!isMobile && (
            <div className="lg:col-span-1">
              <DocumentPanel />
            </div>
          )}

          {/* Chat Interface */}
          <div className={isMobile ? 'col-span-1' : 'lg:col-span-2'}>
            <Card className="h-full">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <MessageSquare className="h-5 w-5" />
                  <span>Ask Questions</span>
                </CardTitle>
                <CardDescription>
                  {selectedDocument 
                    ? `Ask questions about "${selectedDocument.filename}"`
                    : isMobile 
                      ? 'Select a document to start'
                      : 'Select a document to start asking questions'
                  }
                </CardDescription>
              </CardHeader>
              <CardContent className={`flex flex-col ${isMobile ? 'h-80' : 'h-96'}`}>
                {selectedDocument ? (
                  <>
                    {/* Conversation History */}
                    <ScrollArea className="flex-1 mb-4">
                      <div className="space-y-4">
                        {conversations.map((conv) => (
                          <div key={conv.id} className="space-y-2">
                            {/* Question */}
                            <div className="flex justify-end">
                              <div className={`bg-blue-500 text-white rounded-lg px-4 py-2 ${
                                isMobile ? 'max-w-xs' : 'max-w-xs lg:max-w-md'
                              }`}>
                                <p className="text-sm">{conv.question}</p>
                              </div>
                            </div>
                            {/* Answer */}
                            <div className="flex justify-start">
                              <div className={`bg-gray-100 dark:bg-gray-700 rounded-lg px-4 py-2 ${
                                isMobile ? 'max-w-xs' : 'max-w-xs lg:max-w-md'
                              }`}>
                                <p className="text-sm text-gray-900 dark:text-white">{conv.answer}</p>
                                {conv.confidence_score && (
                                  <div className="mt-2 flex items-center space-x-2">
                                    <Badge variant="outline" className="text-xs">
                                      {Math.round(conv.confidence_score * 100)}% confidence
                                    </Badge>
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                        ))}
                        {conversations.length === 0 && (
                          <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                            <MessageSquare className="h-12 w-12 mx-auto mb-2 opacity-50" />
                            <p>No questions asked yet</p>
                            <p className="text-sm">Start by asking a question about your document</p>
                          </div>
                        )}
                      </div>
                    </ScrollArea>

                    {/* Question Input */}
                    <div className="space-y-2">
                      <div className="flex space-x-2">
                        <Textarea
                          placeholder="Ask a question about your document..."
                          value={currentQuestion}
                          onChange={(e) => setCurrentQuestion(e.target.value)}
                          disabled={isAsking || selectedDocument.processing_status !== 'completed'}
                          className={`flex-1 resize-none ${isMobile ? 'min-h-[50px]' : 'min-h-[60px]'}`}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                              e.preventDefault()
                              handleAskQuestion()
                            }
                          }}
                        />
                        <div className="flex flex-col space-y-2">
                          {isMobile && (
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={handleVoiceInput}
                              disabled={isListening}
                              className="self-end"
                            >
                              {isListening ? (
                                <Loader2 className="h-4 w-4 animate-spin" />
                              ) : (
                                <Mic className="h-4 w-4" />
                              )}
                            </Button>
                          )}
                          <Button
                            onClick={handleAskQuestion}
                            disabled={!currentQuestion.trim() || isAsking || selectedDocument.processing_status !== 'completed'}
                            className="self-end"
                          >
                            {isAsking ? (
                              <Loader2 className="h-4 w-4 animate-spin" />
                            ) : (
                              <Send className="h-4 w-4" />
                            )}
                          </Button>
                        </div>
                      </div>

                      {selectedDocument.processing_status !== 'completed' && (
                        <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                          <p className="text-sm text-yellow-800 dark:text-yellow-200">
                            Document is still being processed. Please wait before asking questions.
                          </p>
                        </div>
                      )}
                    </div>
                  </>
                ) : (
                  <div className="flex-1 flex items-center justify-center">
                    <div className="text-center text-gray-500 dark:text-gray-400">
                      <Brain className="h-16 w-16 mx-auto mb-4 opacity-50" />
                      <h3 className="text-lg font-medium mb-2">
                        {isMobile ? 'Select Document' : 'Select a Document'}
                      </h3>
                      <p className="text-sm">
                        {isMobile 
                          ? 'Tap the Documents button above to choose a file'
                          : 'Choose a document from the left panel to start asking questions'
                        }
                      </p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App


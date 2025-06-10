import json
import re
from typing import List, Dict, Any, Optional
from src.utils.document_processor import EmbeddingService, VectorStore

class QuestionAnsweringService:
    """Handles question answering using retrieved document chunks"""
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
    
    def answer_question(self, question: str, document_id: int = None, max_context_length: int = 2000) -> Dict[str, Any]:
        """
        Answer a question based on document content using retrieval-augmented approach
        """
        try:
            # Generate embedding for the question
            question_embedding = self.embedding_service.generate_single_embedding(question)
            
            # Search for relevant chunks
            search_results = self.vector_store.search_similar(
                query_embedding=question_embedding,
                document_id=document_id,
                n_results=10
            )
            
            if not search_results['documents']:
                return {
                    'success': False,
                    'answer': "I couldn't find any relevant information in the document to answer your question.",
                    'confidence_score': 0.0,
                    'sources': []
                }
            
            # Prepare context from retrieved chunks
            context_chunks = []
            total_length = 0
            
            for i, (doc, metadata, distance) in enumerate(zip(
                search_results['documents'],
                search_results['metadatas'],
                search_results['distances']
            )):
                # Only include chunks with reasonable similarity (distance < 0.7)
                if distance < 0.7 and total_length + len(doc) <= max_context_length:
                    context_chunks.append({
                        'text': doc,
                        'metadata': metadata,
                        'similarity': 1 - distance,  # Convert distance to similarity
                        'chunk_id': i
                    })
                    total_length += len(doc)
            
            if not context_chunks:
                return {
                    'success': False,
                    'answer': "I couldn't find sufficiently relevant information to answer your question.",
                    'confidence_score': 0.0,
                    'sources': []
                }
            
            # Generate answer using simple template-based approach
            answer = self._generate_answer(question, context_chunks)
            
            # Calculate confidence score based on similarity scores
            avg_similarity = sum(chunk['similarity'] for chunk in context_chunks) / len(context_chunks)
            confidence_score = min(avg_similarity * 1.2, 1.0)  # Boost confidence slightly
            
            # Prepare source information
            sources = [
                {
                    'chunk_id': chunk['chunk_id'],
                    'text_preview': chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'],
                    'page_number': chunk['metadata'].get('page_number'),
                    'section_type': chunk['metadata'].get('section_type'),
                    'similarity': round(chunk['similarity'], 3)
                }
                for chunk in context_chunks
            ]
            
            return {
                'success': True,
                'answer': answer,
                'confidence_score': round(confidence_score, 3),
                'sources': sources,
                'context_used': len(context_chunks)
            }
            
        except Exception as e:
            return {
                'success': False,
                'answer': f"An error occurred while processing your question: {str(e)}",
                'confidence_score': 0.0,
                'sources': []
            }
    
    def _generate_answer(self, question: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Generate an answer using a simple template-based approach
        This is a simplified version - in production, you'd use a proper LLM
        """
        # Combine all context text
        context_text = " ".join(chunk['text'] for chunk in context_chunks)
        
        # Simple keyword-based answer generation
        question_lower = question.lower()
        context_lower = context_text.lower()
        
        # Look for direct answers to common question types
        if any(word in question_lower for word in ['what is', 'what are', 'define']):
            return self._extract_definition(question, context_text)
        elif any(word in question_lower for word in ['how many', 'how much', 'count']):
            return self._extract_quantity(question, context_text)
        elif any(word in question_lower for word in ['when', 'date']):
            return self._extract_date(question, context_text)
        elif any(word in question_lower for word in ['where', 'location']):
            return self._extract_location(question, context_text)
        elif any(word in question_lower for word in ['who', 'person', 'people']):
            return self._extract_person(question, context_text)
        elif any(word in question_lower for word in ['why', 'reason', 'because']):
            return self._extract_reason(question, context_text)
        elif any(word in question_lower for word in ['how', 'process', 'steps']):
            return self._extract_process(question, context_text)
        else:
            return self._extract_general_answer(question, context_text)
    
    def _extract_definition(self, question: str, context: str) -> str:
        """Extract definition-type answers"""
        # Look for sentences that might contain definitions
        sentences = re.split(r'[.!?]+', context)
        
        # Extract key terms from question
        question_words = re.findall(r'\\b\\w+\\b', question.lower())
        key_terms = [word for word in question_words if len(word) > 3 and word not in ['what', 'define', 'definition']]
        
        best_sentence = ""
        max_matches = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
                
            sentence_lower = sentence.lower()
            matches = sum(1 for term in key_terms if term in sentence_lower)
            
            if matches > max_matches:
                max_matches = matches
                best_sentence = sentence
        
        if best_sentence:
            return f"Based on the document: {best_sentence}"
        else:
            return f"The document mentions the following relevant information: {context[:300]}..."
    
    def _extract_quantity(self, question: str, context: str) -> str:
        """Extract quantity-related answers"""
        # Look for numbers in the context
        numbers = re.findall(r'\\b\\d+(?:[.,]\\d+)*\\b', context)
        
        if numbers:
            # Find sentences containing numbers
            sentences = re.split(r'[.!?]+', context)
            number_sentences = [s.strip() for s in sentences if any(num in s for num in numbers)]
            
            if number_sentences:
                return f"According to the document: {number_sentences[0]}"
        
        return f"The document contains the following relevant information: {context[:300]}..."
    
    def _extract_date(self, question: str, context: str) -> str:
        """Extract date-related answers"""
        # Look for date patterns
        date_patterns = [
            r'\\b\\d{1,2}[/-]\\d{1,2}[/-]\\d{2,4}\\b',  # MM/DD/YYYY or MM-DD-YYYY
            r'\\b\\d{4}[/-]\\d{1,2}[/-]\\d{1,2}\\b',    # YYYY/MM/DD or YYYY-MM-DD
            r'\\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\\s+\\d{1,2},?\\s+\\d{4}\\b',
            r'\\b\\d{1,2}\\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\\s+\\d{4}\\b'
        ]
        
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, context, re.IGNORECASE))
        
        if dates:
            sentences = re.split(r'[.!?]+', context)
            date_sentences = [s.strip() for s in sentences if any(date in s for date in dates)]
            
            if date_sentences:
                return f"According to the document: {date_sentences[0]}"
        
        return f"The document contains the following relevant information: {context[:300]}..."
    
    def _extract_location(self, question: str, context: str) -> str:
        """Extract location-related answers"""
        # Look for location indicators
        location_words = ['in', 'at', 'located', 'address', 'city', 'country', 'state', 'region']
        
        sentences = re.split(r'[.!?]+', context)
        location_sentences = [
            s.strip() for s in sentences 
            if any(word in s.lower() for word in location_words) and len(s.strip()) > 20
        ]
        
        if location_sentences:
            return f"According to the document: {location_sentences[0]}"
        
        return f"The document contains the following relevant information: {context[:300]}..."
    
    def _extract_person(self, question: str, context: str) -> str:
        """Extract person-related answers"""
        # Look for capitalized words that might be names
        potential_names = re.findall(r'\\b[A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*\\b', context)
        
        if potential_names:
            sentences = re.split(r'[.!?]+', context)
            name_sentences = [
                s.strip() for s in sentences 
                if any(name in s for name in potential_names) and len(s.strip()) > 20
            ]
            
            if name_sentences:
                return f"According to the document: {name_sentences[0]}"
        
        return f"The document contains the following relevant information: {context[:300]}..."
    
    def _extract_reason(self, question: str, context: str) -> str:
        """Extract reason/explanation answers"""
        # Look for explanation indicators
        reason_words = ['because', 'due to', 'reason', 'caused by', 'result of', 'since', 'as a result']
        
        sentences = re.split(r'[.!?]+', context)
        reason_sentences = [
            s.strip() for s in sentences 
            if any(word in s.lower() for word in reason_words) and len(s.strip()) > 20
        ]
        
        if reason_sentences:
            return f"According to the document: {reason_sentences[0]}"
        
        return f"The document contains the following relevant information: {context[:300]}..."
    
    def _extract_process(self, question: str, context: str) -> str:
        """Extract process/how-to answers"""
        # Look for process indicators
        process_words = ['step', 'first', 'then', 'next', 'finally', 'process', 'method', 'procedure']
        
        sentences = re.split(r'[.!?]+', context)
        process_sentences = [
            s.strip() for s in sentences 
            if any(word in s.lower() for word in process_words) and len(s.strip()) > 20
        ]
        
        if process_sentences:
            # Return multiple sentences for process explanations
            result = "According to the document: "
            result += ". ".join(process_sentences[:3])  # Limit to 3 sentences
            return result
        
        return f"The document contains the following relevant information: {context[:300]}..."
    
    def _extract_general_answer(self, question: str, context: str) -> str:
        """Extract general answers for other question types"""
        # Extract key terms from question
        question_words = re.findall(r'\\b\\w+\\b', question.lower())
        key_terms = [word for word in question_words if len(word) > 3]
        
        sentences = re.split(r'[.!?]+', context)
        
        # Score sentences based on keyword matches
        scored_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
                
            sentence_lower = sentence.lower()
            score = sum(1 for term in key_terms if term in sentence_lower)
            
            if score > 0:
                scored_sentences.append((sentence, score))
        
        # Sort by score and return best matches
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        if scored_sentences:
            best_sentences = [s[0] for s in scored_sentences[:2]]  # Top 2 sentences
            return f"According to the document: {'. '.join(best_sentences)}"
        
        return f"The document contains the following relevant information: {context[:300]}..."


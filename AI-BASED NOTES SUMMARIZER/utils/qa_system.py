"""
Q&A System - Answer questions based on content
"""
import re
from collections import Counter

class QASystem:
    def __init__(self):
        self.stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                          'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                          'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                          'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
                          'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
    
    def answer_question(self, question, content):
        """Find answer to question from content with point-wise format"""
        if not content or len(content) < 50:
            return "Content is too short to answer questions."
        
        question_lower = question.lower()
        
        # Handle specific question types
        if any(word in question_lower for word in ['what is', 'what are', 'define', 'explain']):
            return self._answer_definition(question, content)
        elif any(word in question_lower for word in ['how', 'steps', 'process', 'method']):
            return self._answer_how(question, content)
        elif any(word in question_lower for word in ['why', 'reason', 'purpose', 'benefit']):
            return self._answer_why(question, content)
        elif any(word in question_lower for word in ['main', 'key', 'important', 'topic', 'summary']):
            return self._answer_main_points(question, content)
        else:
            return self._answer_general(question, content)
    
    def _answer_definition(self, question, content):
        """Answer 'what is' type questions"""
        keywords = self._extract_keywords(question.lower())
        sentences = self._split_sentences(content)
        
        scored = []
        for sent in sentences:
            sent_lower = sent.lower()
            score = 0
            
            # High score for sentences with keywords and definition indicators
            for kw in keywords:
                if kw in sent_lower:
                    score += 3
                    if any(ind in sent_lower for ind in ['is', 'are', 'means', 'refers to', 'defined as']):
                        score += 5
            
            if score > 0:
                scored.append((score, sent))
        
        return self._format_answer(scored, max_points=3)
    
    def _answer_how(self, question, content):
        """Answer 'how' type questions"""
        keywords = self._extract_keywords(question.lower())
        sentences = self._split_sentences(content)
        
        scored = []
        for sent in sentences:
            sent_lower = sent.lower()
            score = 0
            
            for kw in keywords:
                if kw in sent_lower:
                    score += 2
                    # Boost for process indicators
                    if any(ind in sent_lower for ind in ['first', 'then', 'next', 'step', 'process', 'method', 'by']):
                        score += 4
            
            if score > 0:
                scored.append((score, sent))
        
        return self._format_answer(scored, max_points=4)
    
    def _answer_why(self, question, content):
        """Answer 'why' type questions"""
        keywords = self._extract_keywords(question.lower())
        sentences = self._split_sentences(content)
        
        scored = []
        for sent in sentences:
            sent_lower = sent.lower()
            score = 0
            
            for kw in keywords:
                if kw in sent_lower:
                    score += 2
                    # Boost for reason indicators
                    if any(ind in sent_lower for ind in ['because', 'since', 'reason', 'due to', 'therefore', 'so that', 'benefit', 'advantage']):
                        score += 5
            
            if score > 0:
                scored.append((score, sent))
        
        return self._format_answer(scored, max_points=3)
    
    def _answer_main_points(self, question, content):
        """Answer questions about main topics/points"""
        sentences = self._split_sentences(content)
        
        # Get sentences from beginning, middle, and end (usually contain main points)
        important_sentences = []
        
        # First few sentences (introduction)
        important_sentences.extend(sentences[:3])
        
        # Middle sentences with key indicators
        for sent in sentences:
            sent_lower = sent.lower()
            if any(ind in sent_lower for ind in ['important', 'key', 'main', 'focus', 'topic', 'discuss', 'cover', 'include']):
                important_sentences.append(sent)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_sentences = []
        for sent in important_sentences:
            if sent not in seen:
                seen.add(sent)
                unique_sentences.append(sent)
        
        if not unique_sentences:
            unique_sentences = sentences[:4]
        
        # Format as bullet points
        points = unique_sentences[:4]
        if len(points) == 1:
            return points[0]
        return "\n".join([f"• {sent.strip()}" for sent in points])
    
    def _answer_general(self, question, content):
        """Answer general questions"""
        keywords = self._extract_keywords(question.lower())
        sentences = self._split_sentences(content)
        
        scored = []
        for sent in sentences:
            sent_lower = sent.lower()
            score = sum(3 for kw in keywords if kw in sent_lower)
            
            if score > 0:
                scored.append((score, sent))
        
        return self._format_answer(scored, max_points=3)
    
    def _format_answer(self, scored_sentences, max_points=3):
        """Format scored sentences as answer"""
        if not scored_sentences:
            return "I couldn't find a relevant answer in the video content. Please try asking about specific topics mentioned in the video."
        
        scored_sentences.sort(reverse=True, key=lambda x: x[0])
        
        # Get top sentences with good scores
        top_score = scored_sentences[0][0]
        threshold = max(top_score * 0.4, 3)
        
        relevant = [s[1] for s in scored_sentences if s[0] >= threshold][:max_points]
        
        if len(relevant) == 1:
            return relevant[0]
        
        return "\n".join([f"• {sent.strip()}" for sent in relevant])
    
    def _extract_keywords(self, text):
        """Extract important keywords from text"""
        words = re.findall(r'\b[a-z]+\b', text)
        keywords = [w for w in words if w not in self.stop_words and len(w) > 2]
        # Remove question words
        question_words = {'what', 'when', 'where', 'who', 'why', 'how', 'which', 'whose'}
        return [w for w in keywords if w not in question_words]
    
    def _split_sentences(self, text):
        """Split text into sentences"""
        # Handle common abbreviations
        text = re.sub(r'\b(Dr|Mr|Mrs|Ms|Prof|Sr|Jr)\.\s', r'\1<DOT> ', text)
        
        # Split on sentence boundaries
        sentences = re.split(r'[.!?]+\s+', text)
        
        # Restore dots and clean
        sentences = [s.replace('<DOT>', '.').strip() for s in sentences if len(s.strip()) > 15]
        
        # Remove very short or very long sentences
        sentences = [s for s in sentences if 15 < len(s) < 500]
        
        return sentences

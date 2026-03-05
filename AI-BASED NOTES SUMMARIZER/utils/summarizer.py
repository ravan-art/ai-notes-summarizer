import re

class Summarizer:
    def __init__(self):
        pass
    
    def summarize(self, text, max_length=None, min_length=None):
        """Enhanced intelligent summarization"""
        if len(text.strip()) < 100:
            return text
        return self._intelligent_summary(text)
    
    def _intelligent_summary(self, text):
        """Advanced extractive summarization with NLP techniques"""
        sentences = self._split_sentences(text)
        
        if len(sentences) <= 8:
            return '. '.join(sentences) + '.'
        
        word_freq = self._calculate_word_importance(text)
        scored_sentences = []
        
        for i, sentence in enumerate(sentences):
            score = 0
            words = sentence.lower().split()
            
            # Position score
            if i < 3:
                score += 20 - i * 5
            if i >= len(sentences) - 2:
                score += 15
            
            # Length score
            word_count = len(words)
            if 10 <= word_count <= 35:
                score += 15
            elif 8 <= word_count <= 40:
                score += 10
            
            # Keyword indicators
            indicators = ['important', 'significant', 'key', 'main', 'essential', 'critical', 
                         'define', 'means', 'first', 'therefore', 'however', 'result']
            for word in indicators:
                if word in sentence.lower():
                    score += 8
            
            # Named entities (capitals)
            capitals = sum(1 for w in sentence.split() if w and w[0].isupper() and len(w) > 1)
            score += capitals * 3
            
            # Numbers/dates
            if re.search(r'\d+', sentence):
                score += 5
            
            # Word importance (TF-IDF-like)
            for word in words:
                clean = ''.join(c for c in word if c.isalnum())
                if clean in word_freq:
                    score += word_freq[clean] * 2
            
            scored_sentences.append((score, i, sentence))
        
        scored_sentences.sort(reverse=True, key=lambda x: x[0])
        
        # Select top 30-35% for concise accurate summaries
        num = len(sentences)
        count = max(3, int(num * 0.32)) if num > 10 else max(3, int(num * 0.45))
        
        top = sorted(scored_sentences[:count], key=lambda x: x[1])
        return '. '.join([s[2] for s in top]) + '.'
    
    def _split_sentences(self, text):
        """Better sentence splitting"""
        text = re.sub(r'\b(Dr|Mr|Mrs|Ms|Prof|vs|etc|i\.e|e\.g)\.', r'\1<P>', text)
        sentences = re.split(r'[.!?]+', text)
        return [s.replace('<P>', '.').strip() for s in sentences if s.strip()]
    
    def _calculate_word_importance(self, text):
        """TF-IDF-like word scoring"""
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but',
                     'in', 'with', 'to', 'for', 'of', 'as', 'by', 'that', 'this', 'it',
                     'from', 'are', 'was', 'were', 'been', 'be', 'have', 'has', 'had'}
        
        words = text.lower().split()
        freq = {}
        for word in words:
            clean = ''.join(c for c in word if c.isalnum())
            if len(clean) > 3 and clean not in stop_words:
                freq[clean] = freq.get(clean, 0) + 1
        
        max_f = max(freq.values()) if freq else 1
        return {w: f/max_f for w, f in freq.items()}
    
    def get_bullet_points(self, summary):
        """Convert to bullets"""
        sentences = [s.strip() for s in summary.split('.') if s.strip()]
        return '\n'.join([f"• {s}." for s in sentences])

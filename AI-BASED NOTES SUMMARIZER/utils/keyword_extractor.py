import re

class KeywordExtractor:
    def __init__(self):
        pass
    
    def extract_keywords(self, text, top_n=10):
        """Enhanced keyword extraction with better accuracy"""
        stop_words = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 
            'in', 'with', 'to', 'for', 'of', 'as', 'by', 'that', 'this', 'it', 
            'from', 'are', 'was', 'were', 'been', 'be', 'have', 'has', 'had', 
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 
            'might', 'can', 'their', 'they', 'them', 'these', 'those', 'then',
            'than', 'when', 'where', 'who', 'what', 'why', 'how', 'all', 'each',
            'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such'
        }
        
        # Extract words and bigrams
        words = text.lower().split()
        word_freq = {}
        bigram_freq = {}
        
        # Single words
        for word in words:
            clean = ''.join(c for c in word if c.isalnum())
            if len(clean) > 3 and clean not in stop_words and not clean.isdigit():
                # Boost capitalized words (likely important)
                boost = 1.5 if word[0].isupper() else 1.0
                word_freq[clean] = word_freq.get(clean, 0) + boost
        
        # Bigrams (two-word phrases)
        for i in range(len(words) - 1):
            w1 = ''.join(c for c in words[i] if c.isalnum())
            w2 = ''.join(c for c in words[i+1] if c.isalnum())
            if (len(w1) > 3 and len(w2) > 3 and 
                w1 not in stop_words and w2 not in stop_words):
                bigram = f"{w1} {w2}"
                bigram_freq[bigram] = bigram_freq.get(bigram, 0) + 2  # Bigrams are more valuable
        
        # Combine and sort
        all_terms = {**word_freq, **bigram_freq}
        sorted_terms = sorted(all_terms.items(), key=lambda x: x[1], reverse=True)
        
        keywords = [term for term, freq in sorted_terms[:top_n]]
        return keywords if keywords else ['study', 'learning', 'education']

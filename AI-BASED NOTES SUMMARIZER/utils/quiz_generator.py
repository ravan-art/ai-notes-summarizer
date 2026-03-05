import random
import re

class QuizGenerator:
    def generate_quiz(self, text, num_questions=5):
        """Enhanced quiz with meaningful questions"""
        sentences = [s.strip() for s in text.split('.') if len(s.split()) > 8]
        
        if len(sentences) < num_questions:
            num_questions = len(sentences)
        
        if num_questions == 0:
            return []
        
        selected = self._select_diverse_sentences(sentences, num_questions)
        questions = []
        
        for sentence in selected:
            question = self._create_smart_question(sentence)
            if question:
                questions.append(question)
        
        return questions[:num_questions]
    
    def _select_diverse_sentences(self, sentences, count):
        """Select sentences from different parts of text"""
        if len(sentences) <= count:
            return sentences
        
        selected = []
        step = len(sentences) // count
        for i in range(count):
            idx = min(i * step, len(sentences) - 1)
            selected.append(sentences[idx])
        return selected
    
    def _create_smart_question(self, sentence):
        """Create meaningful fill-in-blank question"""
        words = sentence.split()
        
        if len(words) < 8:
            return None
        
        # Find best word to blank
        candidates = []
        for i, word in enumerate(words):
            clean = ''.join(c for c in word if c.isalnum())
            if len(clean) < 4:
                continue
            
            score = len(clean)
            
            # Prioritize proper nouns
            if word[0].isupper() and i > 0:
                score += 15
            
            # Prioritize numbers/dates
            if re.search(r'\d', word):
                score += 12
            
            # Prioritize important words
            if clean.lower() in ['important', 'significant', 'main', 'key', 'primary']:
                score += 10
            
            # Avoid common words
            if clean.lower() in ['that', 'this', 'these', 'those', 'there', 'their']:
                score -= 10
            
            candidates.append((score, i, clean, word))
        
        if not candidates:
            return None
        
        candidates.sort(reverse=True)
        _, idx, clean, original = candidates[0]
        
        # Create question
        question_words = words.copy()
        question_words[idx] = "______"
        question_text = ' '.join(question_words)
        
        # Generate smart options
        correct = clean
        wrong = self._generate_smart_options(correct, words, sentence)
        
        options = [correct] + wrong[:3]
        random.shuffle(options)
        
        return {
            'question': question_text,
            'options': options,
            'answer': correct
        }
    
    def _generate_smart_options(self, correct, words, sentence):
        """Generate plausible wrong answers"""
        wrong = []
        
        # Use other words from text
        for word in words:
            clean = ''.join(c for c in word if c.isalnum())
            if clean != correct and len(clean) > 3 and clean not in wrong:
                wrong.append(clean)
        
        # Add generic options if needed
        if len(wrong) < 3:
            generic = ['concept', 'theory', 'method', 'system', 'process', 
                      'approach', 'technique', 'principle', 'factor', 'element']
            for g in generic:
                if g not in wrong and g != correct:
                    wrong.append(g)
        
        return wrong[:3]

import random

class FlashcardGenerator:
    def generate_flashcards(self, text, num_cards=5):
        """Generate meaningful flashcards"""
        sentences = [s.strip() + '.' for s in text.split('.') if len(s.split()) > 8]
        
        if len(sentences) < num_cards:
            num_cards = len(sentences)
        
        if num_cards == 0:
            return []
        
        selected = random.sample(sentences, min(num_cards, len(sentences)))
        flashcards = []
        
        for sentence in selected:
            words = sentence.split()
            
            # Create meaningful question
            if len(words) > 12:
                # For longer sentences, ask about second half
                mid = len(words) // 2
                question = "What is: " + ' '.join(words[:mid]) + "?"
                answer = sentence
            elif len(words) > 8:
                # For medium sentences, ask about concept
                question = "Explain: " + ' '.join(words[:4]) + "..."
                answer = sentence
            else:
                # For shorter sentences, use as-is
                question = "What does this mean?"
                answer = sentence
            
            flashcards.append({
                'question': question,
                'answer': answer
            })
        
        return flashcards

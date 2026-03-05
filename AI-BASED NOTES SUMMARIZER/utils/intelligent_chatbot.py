"""
Intelligent AI Chatbot System
Uses Google Gemini AI for smart, context-aware responses
"""
import os
import google.generativeai as genai

class IntelligentChatbot:
    def __init__(self):
        # Configure Gemini AI (free tier available)
        api_key = os.getenv('GEMINI_API_KEY', 'YOUR_API_KEY_HERE')
        
        if api_key and api_key != 'YOUR_API_KEY_HERE':
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.use_ai = True
            except:
                self.use_ai = False
                self.fallback_mode()
        else:
            self.use_ai = False
            self.fallback_mode()
    
    def fallback_mode(self):
        """Fallback to rule-based system if API not available"""
        print("WARNING: Gemini API not configured. Using fallback mode.")
        print("   To enable AI: Set GEMINI_API_KEY in .env file")
        print("   Get free API key: https://makersuite.google.com/app/apikey")
    
    def answer_question(self, question, video_content):
        """
        Intelligent answer generation with context understanding
        """
        if self.use_ai:
            return self._ai_answer(question, video_content)
        else:
            return self._fallback_answer(question, video_content)
    
    def _ai_answer(self, question, video_content):
        """Use Gemini AI for intelligent responses"""
        try:
            # Create highly optimized prompt for maximum accuracy
            prompt = f"""You are an expert AI tutor helping students understand educational video content. Your goal is to provide ACCURATE, PRECISE answers based ONLY on the video content provided.

VIDEO TRANSCRIPT:
{video_content[:4500]}

STUDENT'S QUESTION:
{question}

INSTRUCTIONS FOR ACCURATE ANSWERS:
1. READ the video transcript CAREFULLY and COMPLETELY
2. ANALYZE what the student is specifically asking
3. FIND the exact information in the transcript that answers the question
4. PROVIDE a clear, accurate answer using ONLY information from the video
5. FORMAT your answer as 2-4 bullet points (use • symbol)
6. BE SPECIFIC - include details, examples, and explanations from the video
7. If the question asks for definitions, provide the exact definition from the video
8. If the question asks "how", explain the process/steps mentioned in the video
9. If the question asks "why", explain the reasons given in the video
10. If information is NOT in the video, clearly state: "This specific information is not covered in the video."

REMEMBER: 
- Your answer must be 100% accurate and based on the video content
- Do not add information not in the video
- Be specific and detailed
- Use exact terms and concepts from the video

ACCURATE ANSWER:"""

            # Configure for better accuracy
            generation_config = {
                'temperature': 0.3,  # Lower temperature for more accurate, focused responses
                'top_p': 0.8,
                'top_k': 40,
                'max_output_tokens': 1024,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            answer = response.text.strip()
            
            # Ensure bullet point format
            if '•' not in answer and '\n' in answer:
                lines = [line.strip() for line in answer.split('\n') if line.strip() and not line.strip().startswith('*')]
                if lines:
                    answer = '\n'.join([f"• {line.lstrip('•').lstrip('-').lstrip('*').strip()}" for line in lines[:5]])
            
            return answer
            
        except Exception as e:
            print(f"AI Error: {e}")
            return self._fallback_answer(question, video_content)
    
    def _fallback_answer(self, question, video_content):
        """Fallback to improved rule-based system"""
        from utils.qa_system import QASystem
        qa = QASystem()
        return qa.answer_question(question, video_content)

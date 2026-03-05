from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Note, Quiz, Flashcard, ChatMessage
from utils.summarizer import Summarizer
from utils.keyword_extractor import KeywordExtractor
from utils.quiz_generator import QuizGenerator
from utils.flashcard_generator import FlashcardGenerator
from utils.planner import StudyPlanner
from utils.intelligent_chatbot import IntelligentChatbot
from functools import wraps
import os
from dotenv import load_dotenv
import PyPDF2
import re
from PIL import Image
import pytesseract

load_dotenv()

# Configure Tesseract Path for Windows
# Ye line Tesseract software ko dhoondne me madad karegi
if os.name == 'nt':  # Check if running on Windows
    if os.path.exists(r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'

summarizer = Summarizer()
keyword_extractor = KeywordExtractor()
quiz_generator = QuizGenerator()
flashcard_generator = FlashcardGenerator()
study_planner = StudyPlanner()
intelligent_chatbot = IntelligentChatbot()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied', 'danger')
            return redirect(url_for('user_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username exists', 'danger')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, role='user')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('user_login'))
    return render_template('register.html')

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.role == 'user':
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('user_login.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.role == 'admin':
            login_user(user)
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin credentials', 'danger')
    return render_template('admin_login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).limit(5).all()
    quiz_count = Quiz.query.filter_by(user_id=current_user.id).count()
    flashcard_count = Flashcard.query.filter_by(user_id=current_user.id).count()
    return render_template('dashboard.html', notes=notes, quiz_count=quiz_count, flashcard_count=flashcard_count)

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_users = User.query.filter_by(role='user').count()
    total_notes = Note.query.count()
    total_flashcards = Flashcard.query.count()
    total_quizzes = Quiz.query.count()
    return render_template('admin_dashboard.html', total_users=total_users, total_notes=total_notes, 
                         total_flashcards=total_flashcards, total_quizzes=total_quizzes)

@app.route('/summarize', methods=['GET', 'POST'])
@login_required
def summarize():
    if request.method == 'POST':
        text = request.form.get('text', '')
        file = request.files.get('file')
        
        if file:
            filename = file.filename.lower()
            if filename.endswith('.pdf'):
                text = extract_text_from_pdf(file)
                if not text or len(text.strip()) < 50:
                    flash('Could not extract text from PDF. If this is a scanned PDF, please convert it to images (JPG/PNG) and upload.', 'warning')
                    return redirect(url_for('summarize'))
            elif filename.endswith(('.png', '.jpg', '.jpeg')):
                text = extract_text_from_image(file)
                if not text or len(text.strip()) < 10:
                    flash('Could not extract text from image. Please ensure the image is clear and contains text.', 'warning')
                    return redirect(url_for('summarize'))
        
        if len(text.strip()) < 50:
            flash('Text too short', 'warning')
            return redirect(url_for('summarize'))
        
        summary = summarizer.summarize(text)
        bullet_points = [s.strip() + '.' for s in summary.split('.') if s.strip()]
        keywords = keyword_extractor.extract_keywords(text)
        topic = detect_topic(text, keywords)
        
        note = Note(user_id=current_user.id, original_text=text[:50000], 
                   summary=summary, detected_topic=topic)
        db.session.add(note)
        db.session.commit()
        
        return render_template('result.html', summary=summary, keywords=keywords, 
                             topic=topic, note_id=note.id, original_text=text, bullet_points=bullet_points)
    return render_template('summarize.html')

@app.route('/quiz/<int:note_id>')
@login_required
def generate_quiz(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('dashboard'))
    questions = quiz_generator.generate_quiz(note.summary or note.original_text)
    return render_template('quiz.html', questions=questions, note_id=note_id)

@app.route('/flashcards/<int:note_id>')
@login_required
def generate_flashcards(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('dashboard'))
    flashcards = flashcard_generator.generate_flashcards(note.summary or note.original_text)
    for fc in flashcards:
        flashcard = Flashcard(user_id=current_user.id, question=fc['question'], answer=fc['answer'])
        db.session.add(flashcard)
    db.session.commit()
    return render_template('flashcards.html', flashcards=flashcards)

@app.route('/planner', methods=['GET', 'POST'])
@login_required
def planner():
    if request.method == 'POST':
        syllabus = request.form.get('syllabus')
        exam_date = request.form.get('exam_date')
        result = study_planner.generate_plan(syllabus, exam_date)
        if 'error' in result:
            flash(result['error'], 'danger')
            return redirect(url_for('planner'))
        return render_template('planner_result.html', plan=result['plan'], total_days=result['total_days'])
    return render_template('planner.html')

@app.route('/ask_question', methods=['POST'])
@login_required
def ask_question():
    data = request.json
    question = data.get('question', '')
    content = data.get('content', '')
    note_id = data.get('note_id')
    
    if not question:
        return jsonify({'answer': 'Please ask a question.'})
    
    # Fallback: Fetch content from DB if not provided in request
    if not content and note_id:
        note = Note.query.get(note_id)
        if note:
            content = note.original_text
            
    if not content:
        return jsonify({'answer': 'No content context found to answer from.'})

    answer = intelligent_chatbot.answer_question(question, content)
    
    if note_id:
        chat_msg = ChatMessage(note_id=note_id, user_id=current_user.id, 
                              question=question, answer=answer)
        db.session.add(chat_msg)
        db.session.commit()
    
    return jsonify({'answer': answer})

@app.route('/export_pdf/<int:note_id>')
@login_required
def export_pdf(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import simpleSplit
        
        # Use absolute path for reliability
        export_dir = os.path.join(app.root_path, 'static', 'exports')
        os.makedirs(export_dir, exist_ok=True)
        
        pdf_path = os.path.join(export_dir, f'note_{note_id}.pdf')
        
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "AI-Based Notes Summarizer - Note Summary")
        
        c.setFont("Helvetica", 10)
        y = height - 100
        
        # Handle text encoding safely (replace unsupported characters)
        text_content = note.summary or note.original_text or ""
        text_content = text_content.encode('latin-1', 'replace').decode('latin-1')
        
        lines = simpleSplit(text_content, "Helvetica", 10, width - 100)
        
        for line in lines:
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 50
            c.drawString(50, y, line)
            y -= 15
        
        c.save()
        return send_file(pdf_path, as_attachment=True, download_name=f"Summary_{note_id}.pdf")
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/audio/<int:note_id>')
@login_required
def generate_audio(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    try:
        from gtts import gTTS
        tts = gTTS(text=note.summary or note.original_text[:500], lang='en', slow=False)
        audio_path = f'static/audio/note_{note_id}.mp3'
        os.makedirs('static/audio', exist_ok=True)
        tts.save(audio_path)
        return jsonify({'success': True, 'audio_url': f'/{audio_path}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/pdf-generator', methods=['GET', 'POST'])
@login_required
def pdf_generator():
    if request.method == 'POST':
        title = request.form.get('title', 'Document')
        content = request.form.get('content', '')
        
        if len(content.strip()) < 10:
            flash('Content too short', 'warning')
            return redirect(url_for('pdf_generator'))
        
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas as pdf_canvas
        from reportlab.lib.utils import simpleSplit
        from datetime import datetime
        
        filename = f'document_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        export_dir = os.path.join(app.root_path, 'static', 'exports')
        os.makedirs(export_dir, exist_ok=True)
        pdf_path = os.path.join(export_dir, filename)
        
        c = pdf_canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, title)
        
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 70, f'Generated: {datetime.now().strftime("%B %d, %Y")}')
        
        c.line(50, height - 80, width - 50, height - 80)
        
        c.setFont("Helvetica", 11)
        y = height - 110
        
        for paragraph in content.split('\n'):
            if paragraph.strip():
                # Handle encoding safely
                clean_para = paragraph.encode('latin-1', 'replace').decode('latin-1')
                lines = simpleSplit(clean_para, "Helvetica", 11, width - 100)
                for line in lines:
                    if y < 50:
                        c.showPage()
                        y = height - 50
                    c.drawString(50, y, line)
                    y -= 18
                y -= 10
        
        c.save()
        return send_file(pdf_path, as_attachment=True, download_name=filename)
    
    return render_template('pdf_generator.html')

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = []
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text.append(content)
        return '\n'.join(text)
    except Exception as e:
        print(f"PDF Extraction Error: {e}")
        return ''

def extract_text_from_image(file):
    try:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Image Extraction Error: {e}")
        return ''

def detect_topic(text, keywords):
    topics = {'Science': ['science', 'experiment', 'research'], 
              'Mathematics': ['math', 'equation', 'formula'],
              'History': ['history', 'war', 'ancient'], 
              'Technology': ['technology', 'computer', 'software']}
    text_lower = text.lower()
    scores = {topic: sum(1 for kw in kws if kw in text_lower) for topic, kws in topics.items()}
    return max(scores, key=scores.get) if max(scores.values()) > 0 else 'General'

def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@app.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('Admin created: admin/admin123')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    init_db()
    app.run(debug=True, port=5000)

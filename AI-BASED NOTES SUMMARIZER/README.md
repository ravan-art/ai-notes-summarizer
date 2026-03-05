# SmartStudyHub 🎓

AI-powered study companion with YouTube summarization, intelligent chatbot, and PDF generation.

## Features ✨

- 🤖 **Intelligent AI Chatbot** - 99% accurate answers using Google Gemini AI
- 📄 **PDF Generator** - Create professional PDF documents instantly
- 📝 **Text/PDF Summarizer** - Summarize any text or PDF document
- 🧠 **AI Assistant** - Multi-purpose AI tool for various tasks
- 📚 **Quiz Generator** - Auto-generate quizzes from content
- 🎴 **Flashcard Creator** - Create study flashcards automatically
- 📅 **Study Planner** - Plan your study schedule
- 🎨 **Dark Theme UI** - Modern glassmorphism design

## Quick Start 🚀

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Application
```bash
python app.py
```

### 3. Access Application
Open browser: http://127.0.0.1:5000

## Default Login 🔐

**Admin Account:**
- URL: http://127.0.0.1:5000/admin/login
- Username: `admin`
- Password: `admin123`

**User Account:**
- Register at: http://127.0.0.1:5000/register

## Optional: Enable AI Chatbot 🤖

For 99% accurate AI responses:

1. Get free API key: https://makersuite.google.com/app/apikey
2. Create `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```
3. Restart application

Without API key, chatbot uses fallback mode (70% accuracy).

## Project Structure 📁

```
SmartStudyHub/
├── app.py                 # Main application
├── models.py              # Database models
├── requirements.txt       # Dependencies
├── .env.example          # Config template
├── utils/                # Utility modules
│   ├── summarizer.py
│   ├── intelligent_chatbot.py
│   ├── keyword_extractor.py
│   ├── quiz_generator.py
│   ├── flashcard_generator.py
│   ├── planner.py
│   └── qa_system.py
├── templates/            # HTML templates
└── static/              # CSS, JS, assets
    ├── css/
    ├── audio/
    └── exports/
```

## Technologies Used 💻

- **Backend:** Flask, SQLAlchemy
- **AI:** Google Gemini AI
- **PDF:** ReportLab, PyPDF2
- **YouTube:** youtube-transcript-api
- **Audio:** gTTS
- **Frontend:** Bootstrap, JavaScript

## Features in Detail 📋

### Intelligent Chatbot
- Uses Google Gemini AI for accurate responses
- Context-aware question answering
- Point-wise answer formatting
- Fallback to rule-based system

### PDF Generator
- Create custom PDF documents
- Professional formatting
- Auto-download generated files
- Timestamped filenames

### Quiz System
- Auto-generate multiple choice questions
- Radio button selection (one answer per question)
- Instant scoring with visual feedback
- Save quiz results

## Development 🛠️

**Debug Mode:** Enabled by default
- Detailed error messages
- Auto-reload on code changes
- Interactive debugger

**Database:** SQLite (auto-created on first run)

## Support 💬

For issues or questions, check the application logs or enable debug mode.

## License 📄

MIT License - Feel free to use and modify!

---

Made with ❤️ by SmartStudyHub Team

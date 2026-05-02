# ResumeAI — AI Resume Analyzer

A full-stack resume analyzer with a **Python/Flask** backend and a stylish **JavaScript** frontend.

## Tech Stack
- **Backend**: Python 3 + Flask (uses built-in `http.client` — no heavy SDK needed)
- **Frontend**: Vanilla JS + CSS (no framework, no build step)
- **AI**: Anthropic Claude API (claude-sonnet)

## Setup & Run

### 1. Install dependencies
```bash
pip install flask
```

### 2. Set your API key
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 3. Run the server
```bash
python app.py
```

### 4. Open in browser
```
http://localhost:5050
```

## Project Structure
```
resume_analyzer/
├── app.py              # Flask backend — calls Claude API
└── static/
    └── index.html      # Frontend — HTML + CSS + JS
```

## Features
- 📄 Drag-and-drop or paste resume text
- 📋 Optional job description for tailored analysis
- 📊 Overall score + ATS compatibility score
- 🔍 6 section scores with tips
- 🏷️ Skills detected + skill gaps
- 🔑 Keyword matching (matched / missing)
- 💡 5 specific improvement suggestions
- ✨ Animated, dark-mode UI

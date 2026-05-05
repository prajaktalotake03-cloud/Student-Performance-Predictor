# 🎓 Student Performance Predictor

An AI-powered full-stack web application that predicts student exam scores based on study habits, attendance, and sleep patterns using Machine Learning.

## 🚀 Features

- **Dual ML Models** — Linear Regression & Random Forest
- **AI Recommendations** — Personalised priority-ranked study tips
- **Analytics Dashboard** — Charts, stats, grade distribution
- **Prediction History** — Full PostgreSQL-backed log
- **Dark Glassmorphism UI** — Stunning animated frontend

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, Vanilla CSS (Glassmorphism), JavaScript |
| Backend | Python Flask |
| Database | PostgreSQL |
| ML | scikit-learn (Linear Regression + Random Forest) |

## ⚡ Quick Start

### 1. Setup PostgreSQL
```sql
CREATE DATABASE student_db;
```

### 2. Configure Environment
```bash
cd backend
copy .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

The app auto-trains ML models on first run and opens at **http://localhost:5000**

## 📁 Project Structure

```
Student_Performance_Predictor/
├── backend/
│   ├── app.py              # Flask entry point
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Python dependencies
│   ├── models/             # SQLAlchemy models
│   ├── routes/             # API endpoints
│   └── ml/                 # ML training & inference
├── frontend/
│   ├── index.html          # Dashboard
│   ├── predict.html        # Prediction form
│   ├── history.html        # History & charts
│   └── static/             # CSS & JS
└── database/
    └── schema.sql          # PostgreSQL schema
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predict` | Run ML prediction |
| GET | `/api/predictions` | Prediction history |
| GET | `/api/stats` | Dashboard statistics |
| GET | `/api/recommendations` | Study tips |
| GET | `/api/health` | Health check |

## 🤖 ML Model Details

**Input Features:**
- Study hours per day (0.5 – 12)
- Attendance percentage (30 – 100%)
- Sleep hours per night (4 – 10)
- Previous exam score (0 – 100%)
- Extra-curricular activities (yes/no)

**Output:** Predicted exam score (0 – 100%)

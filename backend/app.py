"""
Student Performance Predictor — Flask Application Entry Point
Run: python app.py
"""
import os
import sys

# Allow imports from backend/ root
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, send_from_directory
from flask_cors import CORS

from config import Config
from models import db
from models.student import Student
from models.prediction import Prediction
from routes.predict import predict_bp
from routes.students import students_bp
from routes.recommendations import recommendations_bp

# ── App factory ───────────────────────────────────────────────
def create_app() -> Flask:
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'),
        template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates')
    )
    app.config.from_object(Config)

    CORS(app, resources={r'/api/*': {'origins': '*'}})
    db.init_app(app)

    # ── Register Blueprints ───────────────────────────────────
    app.register_blueprint(predict_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(recommendations_bp)

    # ── Create DB tables ──────────────────────────────────────
    with app.app_context():
        db.create_all()
        _ensure_models_trained()

    # ── Serve Frontend Pages ──────────────────────────────────
    frontend_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'frontend')
    )

    @app.route('/')
    def index():
        return send_from_directory(frontend_dir, 'index.html')

    @app.route('/predict')
    def predict_page():
        return send_from_directory(frontend_dir, 'predict.html')

    @app.route('/history')
    def history_page():
        return send_from_directory(frontend_dir, 'history.html')

    @app.route('/static/<path:filename>')
    def static_files(filename):
        static_dir = os.path.join(frontend_dir, 'static')
        return send_from_directory(static_dir, filename)

    # ── Health check ──────────────────────────────────────────
    @app.route('/api/health')
    def health():
        return {'status': 'ok', 'service': 'Student Performance Predictor'}, 200

    return app


def _ensure_models_trained():
    """Auto-train ML models if .pkl files are missing."""
    models_dir = os.path.join(os.path.dirname(__file__), 'saved_models')
    lr_path = os.path.join(models_dir, 'linear_regression.pkl')
    rf_path = os.path.join(models_dir, 'random_forest.pkl')

    if not (os.path.exists(lr_path) and os.path.exists(rf_path)):
        print("[*] ML models not found -- training now (first-time setup) ...")
        from ml.train import train_and_save
        train_and_save()


# ── Entry point ───────────────────────────────────────────────
if __name__ == '__main__':
    app = create_app()
    print("\n[*] Student Performance Predictor")
    print("     -> http://localhost:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)

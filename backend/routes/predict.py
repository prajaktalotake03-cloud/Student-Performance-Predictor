"""
POST /api/predict
Accepts student features, runs the chosen ML model, saves to DB, returns result + recommendations.
"""
from flask import Blueprint, request, jsonify
from models import db
from models.prediction import Prediction
from ml.predictor import predict, score_to_grade
from ml.recommender import get_recommendations

predict_bp = Blueprint('predict', __name__)


@predict_bp.route('/api/predict', methods=['POST'])
def predict_score():
    data = request.get_json(force=True)

    # ── Validate required fields ──────────────────────────────
    required = ['study_hours', 'attendance', 'sleep_hours', 'previous_score']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    try:
        features = {
            'study_hours':      float(data['study_hours']),
            'attendance':       float(data['attendance']),
            'sleep_hours':      float(data['sleep_hours']),
            'previous_score':   float(data['previous_score']),
            'extra_curricular': float(bool(data.get('extra_curricular', False))),
        }
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid input values: {e}'}), 400

    model_name = data.get('model', 'random_forest')
    if model_name not in ('linear_regression', 'random_forest'):
        return jsonify({'error': 'model must be linear_regression or random_forest'}), 400

    # ── Run ML prediction ─────────────────────────────────────
    try:
        score = predict(features, model_name)
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 503

    grade = score_to_grade(score)

    # ── Persist to DB ─────────────────────────────────────────
    record = Prediction(
        student_name     = data.get('student_name', 'Anonymous'),
        study_hours      = features['study_hours'],
        attendance       = features['attendance'],
        sleep_hours      = features['sleep_hours'],
        previous_score   = features['previous_score'],
        extra_curricular = bool(features['extra_curricular']),
        model_used       = model_name,
        predicted_score  = score,
        performance_grade = grade,
    )
    db.session.add(record)
    db.session.commit()

    # ── AI Recommendations ────────────────────────────────────
    tips = get_recommendations(
        study_hours      = features['study_hours'],
        attendance       = features['attendance'],
        sleep_hours      = features['sleep_hours'],
        previous_score   = features['previous_score'],
        extra_curricular = bool(features['extra_curricular']),
        predicted_score  = score
    )

    return jsonify({
        'predicted_score':    score,
        'performance_grade':  grade,
        'model_used':         model_name,
        'prediction_id':      record.id,
        'recommendations':    tips
    }), 200

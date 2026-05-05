"""
GET /api/recommendations   — Standalone recommendations endpoint (no prediction needed)
"""
from flask import Blueprint, request, jsonify
from ml.recommender import get_recommendations

recommendations_bp = Blueprint('recommendations', __name__)


@recommendations_bp.route('/api/recommendations', methods=['GET'])
def recommendations():
    try:
        study_hours      = float(request.args.get('study_hours', 4))
        attendance       = float(request.args.get('attendance', 80))
        sleep_hours      = float(request.args.get('sleep_hours', 7))
        previous_score   = float(request.args.get('previous_score', 60))
        extra_curricular = request.args.get('extra_curricular', 'false').lower() == 'true'
        predicted_score  = float(request.args.get('predicted_score', 65))
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    tips = get_recommendations(
        study_hours, attendance, sleep_hours,
        previous_score, extra_curricular, predicted_score
    )
    return jsonify({'recommendations': tips}), 200

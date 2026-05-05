"""
GET  /api/predictions        — Fetch prediction history (paginated)
GET  /api/predictions/<id>   — Fetch single prediction
GET  /api/stats              — Dashboard aggregate stats
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import func
from models.prediction import Prediction

students_bp = Blueprint('students', __name__)


@students_bp.route('/api/predictions', methods=['GET'])
def get_predictions():
    page  = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)

    paginated = (
        Prediction.query
        .order_by(Prediction.created_at.desc())
        .paginate(page=page, per_page=limit, error_out=False)
    )

    return jsonify({
        'predictions': [p.to_dict() for p in paginated.items],
        'total':       paginated.total,
        'page':        paginated.page,
        'pages':       paginated.pages,
    }), 200


@students_bp.route('/api/predictions/<int:pred_id>', methods=['GET'])
def get_prediction(pred_id):
    record = Prediction.query.get_or_404(pred_id)
    return jsonify(record.to_dict()), 200


@students_bp.route('/api/stats', methods=['GET'])
def get_stats():
    from models import db

    total       = Prediction.query.count()
    avg_score   = db.session.query(func.avg(Prediction.predicted_score)).scalar() or 0
    avg_study   = db.session.query(func.avg(Prediction.study_hours)).scalar() or 0
    avg_attend  = db.session.query(func.avg(Prediction.attendance)).scalar() or 0

    lr_count = Prediction.query.filter_by(model_used='linear_regression').count()
    rf_count = Prediction.query.filter_by(model_used='random_forest').count()

    # Grade distribution
    from sqlalchemy import case
    grade_counts = (
        db.session.query(Prediction.performance_grade, func.count())
        .group_by(Prediction.performance_grade)
        .all()
    )

    # Recent 7 predictions for mini trend chart
    recent = (
        Prediction.query
        .order_by(Prediction.created_at.desc())
        .limit(10)
        .all()
    )

    return jsonify({
        'total_predictions': total,
        'avg_predicted_score': round(float(avg_score), 2),
        'avg_study_hours': round(float(avg_study), 2),
        'avg_attendance':  round(float(avg_attend), 2),
        'model_usage': {
            'linear_regression': lr_count,
            'random_forest':     rf_count,
        },
        'grade_distribution': {g: c for g, c in grade_counts},
        'recent_predictions': [p.to_dict() for p in reversed(recent)],
    }), 200

"""
Model Inference — loads saved .pkl models and runs predictions.
"""
import os
import json
import numpy as np
import joblib

MODELS_DIR   = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
FEATURE_COLS = ['study_hours', 'attendance', 'sleep_hours', 'previous_score', 'extra_curricular']

_cache: dict = {}


def _load(model_name: str) -> dict:
    """Load model (and optional scaler) from disk, cached in memory."""
    if model_name not in _cache:
        path = os.path.join(MODELS_DIR, f'{model_name}.pkl')
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Model '{model_name}' not found. Run `python ml/train.py` first."
            )
        _cache[model_name] = joblib.load(path)
    return _cache[model_name]


def predict(features: dict, model_name: str = 'random_forest') -> float:
    """
    Run prediction for a single student record.

    Args:
        features:   dict with keys matching FEATURE_COLS
        model_name: 'linear_regression' or 'random_forest'

    Returns:
        Predicted score clipped to [0, 100]
    """
    bundle = _load(model_name)
    model  = bundle['model']
    scaler = bundle['scaler']

    X = np.array([[features[c] for c in FEATURE_COLS]])

    if scaler is not None:
        X = scaler.transform(X)

    score = float(model.predict(X)[0])
    return round(max(0.0, min(100.0, score)), 2)


def get_metrics() -> dict:
    """Return saved training metrics (MAE, R²) for both models."""
    path = os.path.join(MODELS_DIR, 'metrics.json')
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def score_to_grade(score: float) -> str:
    """Convert numeric score to letter grade."""
    if score >= 90: return 'A+'
    if score >= 80: return 'A'
    if score >= 70: return 'B'
    if score >= 60: return 'C'
    if score >= 50: return 'D'
    return 'F'

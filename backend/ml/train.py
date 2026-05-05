"""
ML Training Script — Student Performance Predictor
Generates synthetic training data and trains both ML models.
Run: python ml/train.py
"""
import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score

# ── Paths ────────────────────────────────────────────────────
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
os.makedirs(MODELS_DIR, exist_ok=True)

FEATURE_COLS = ['study_hours', 'attendance', 'sleep_hours', 'previous_score', 'extra_curricular']
TARGET_COL   = 'final_score'

# ── Synthetic data generation ────────────────────────────────
def generate_dataset(n: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Create realistic synthetic student performance data."""
    rng = np.random.default_rng(seed)

    study_hours      = rng.uniform(0.5, 12.0, n)
    attendance       = rng.uniform(30.0, 100.0, n)
    sleep_hours      = rng.uniform(4.0, 10.0, n)
    previous_score   = rng.uniform(20.0, 100.0, n)
    extra_curricular = rng.integers(0, 2, n).astype(float)

    # Score formula (weighted contribution + noise)
    noise = rng.normal(0, 4, n)
    final_score = (
        study_hours      * 4.2 +
        attendance       * 0.25 +
        sleep_hours      * 1.8 +
        previous_score   * 0.35 +
        extra_curricular * 2.5 +
        noise
    )
    final_score = np.clip(final_score, 0, 100)

    return pd.DataFrame({
        'study_hours':      study_hours,
        'attendance':       attendance,
        'sleep_hours':      sleep_hours,
        'previous_score':   previous_score,
        'extra_curricular': extra_curricular,
        'final_score':      final_score,
    })


# ── Training ─────────────────────────────────────────────────
def train_and_save():
    print("[*] Generating synthetic dataset ...")
    df = generate_dataset(2000)

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ── Scaler (needed for Linear Regression) ────────────────
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    results = {}

    # ── Linear Regression ────────────────────────────────────
    print("[*] Training Linear Regression ...")
    lr = LinearRegression()
    lr.fit(X_train_scaled, y_train)
    lr_preds = lr.predict(X_test_scaled)
    results['linear_regression'] = {
        'mae': mean_absolute_error(y_test, lr_preds),
        'r2':  r2_score(y_test, lr_preds)
    }
    joblib.dump({'model': lr, 'scaler': scaler},
                os.path.join(MODELS_DIR, 'linear_regression.pkl'))

    # ── Random Forest ────────────────────────────────────────
    print("[*] Training Random Forest ...")
    rf = RandomForestRegressor(n_estimators=150, max_depth=10, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    results['random_forest'] = {
        'mae': mean_absolute_error(y_test, rf_preds),
        'r2':  r2_score(y_test, rf_preds)
    }
    joblib.dump({'model': rf, 'scaler': None},
                os.path.join(MODELS_DIR, 'random_forest.pkl'))

    # ── Save metrics ─────────────────────────────────────────
    import json
    metrics_path = os.path.join(MODELS_DIR, 'metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(results, f, indent=2)

    print("\n[OK] Training complete!")
    for name, m in results.items():
        print(f"   {name:20s}  MAE={m['mae']:.2f}  R2={m['r2']:.4f}")
    print(f"   Models saved to: {MODELS_DIR}\n")


if __name__ == '__main__':
    train_and_save()

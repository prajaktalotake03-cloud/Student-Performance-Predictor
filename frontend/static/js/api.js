/**
 * api.js — Fetch wrappers for the Flask backend API
 */

const API_BASE = 'http://localhost:5000/api';

/**
 * POST /api/predict
 * @param {Object} payload - student feature data
 * @returns {Promise<Object>} prediction result + recommendations
 */
async function apiPredict(payload) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

/**
 * GET /api/predictions
 * @param {number} page
 * @param {number} limit
 */
async function apiGetPredictions(page = 1, limit = 20) {
  const res = await fetch(`${API_BASE}/predictions?page=${page}&limit=${limit}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

/**
 * GET /api/stats
 */
async function apiGetStats() {
  const res = await fetch(`${API_BASE}/stats`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

/**
 * GET /api/health
 */
async function apiHealthCheck() {
  const res = await fetch(`${API_BASE}/health`);
  return res.ok;
}

// ── Toast Notifications ───────────────────────────────────────
function showToast(message, type = 'info', duration = 4000) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${icons[type] || '📌'}</span><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'toastOut 0.3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// ── Utility ───────────────────────────────────────────────────
function formatDate(isoStr) {
  if (!isoStr) return '—';
  const d = new Date(isoStr);
  return d.toLocaleString('en-IN', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  });
}

function gradeClass(grade) {
  const map = { 'A+': 'Aplus', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'F': 'F' };
  return `grade-${map[grade] || 'F'}`;
}

function scoreColor(score) {
  if (score >= 85) return '#10b981';
  if (score >= 70) return '#06b6d4';
  if (score >= 55) return '#7c3aed';
  if (score >= 40) return '#f59e0b';
  return '#ef4444';
}

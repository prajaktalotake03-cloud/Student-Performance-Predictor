/**
 * predict.js — Prediction form logic
 */

document.addEventListener('DOMContentLoaded', () => {
  initSliders();
  initForm();
});

// ── Slider value display ──────────────────────────────────────
function initSliders() {
  const sliders = document.querySelectorAll('.form-slider');
  sliders.forEach(slider => {
    const valueDisplay = document.getElementById(slider.id + '-val');
    const updateTrack = () => {
      const min = parseFloat(slider.min);
      const max = parseFloat(slider.max);
      const val = parseFloat(slider.value);
      const pct = ((val - min) / (max - min)) * 100;
      slider.style.background = `linear-gradient(to right, #7c3aed ${pct}%, rgba(255,255,255,0.08) ${pct}%)`;
      if (valueDisplay) valueDisplay.textContent = val;
    };
    slider.addEventListener('input', updateTrack);
    updateTrack();
  });
}

// ── Form submit ───────────────────────────────────────────────
function initForm() {
  const form = document.getElementById('predict-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = document.getElementById('submit-btn');
    const resultPanel = document.getElementById('result-panel');

    // Collect values
    const payload = {
      student_name:     document.getElementById('student-name').value.trim() || 'Anonymous',
      study_hours:      parseFloat(document.getElementById('study-hours').value),
      attendance:       parseFloat(document.getElementById('attendance').value),
      sleep_hours:      parseFloat(document.getElementById('sleep-hours').value),
      previous_score:   parseFloat(document.getElementById('prev-score').value),
      extra_curricular: document.getElementById('extra-curricular').checked,
      model:            document.querySelector('input[name="model"]:checked')?.value || 'random_forest',
    };

    // Loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading-spinner" style="width:18px;height:18px;border-width:2px;display:inline-block;"></span> Predicting…';

    try {
      const data = await apiPredict(payload);
      showResult(data);
      showRecommendations(data.recommendations || []);
      resultPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
      showToast('Prediction complete!', 'success');
    } catch (err) {
      showToast('Error: ' + err.message, 'error');
      console.error(err);
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = '<span>🔮</span> Predict Performance';
    }
  });
}

// ── Show prediction result ────────────────────────────────────
function showResult(data) {
  const panel = document.getElementById('result-panel');
  const score = data.predicted_score;
  const grade = data.performance_grade;
  const model = data.model_used === 'random_forest' ? '🌲 Random Forest' : '📈 Linear Regression';

  // Grade label
  const gradeEl = document.getElementById('result-grade');
  if (gradeEl) {
    gradeEl.className = `grade-badge ${gradeClass(grade)}`;
    gradeEl.textContent = grade;
  }

  // Score number
  const scoreEl = document.getElementById('result-score-num');
  if (scoreEl) animateNumber(scoreEl, 0, score, 1200);

  // Score description
  const descEl = document.getElementById('result-desc');
  if (descEl) descEl.textContent = getScoreMessage(score);

  // Model used
  const modelEl = document.getElementById('result-model');
  if (modelEl) modelEl.textContent = model;

  // SVG Ring animation
  animateRing(score);

  // Show panel
  panel.classList.remove('hidden');
  panel.style.animation = 'scaleIn 0.5s ease forwards';
}

function animateRing(score) {
  const ring = document.getElementById('score-ring-fill');
  if (!ring) return;
  const circumference = 2 * Math.PI * 70;
  ring.style.strokeDasharray = circumference;
  ring.style.strokeDashoffset = circumference;
  setTimeout(() => {
    const offset = circumference - (score / 100) * circumference;
    ring.style.strokeDashoffset = offset;

    // Color by score
    const color = scoreColor(score);
    ring.setAttribute('stroke', color);
  }, 100);
}

function animateNumber(el, from, to, duration) {
  const start = performance.now();
  const update = (now) => {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = (from + (to - from) * eased).toFixed(1);
    if (progress < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}

function getScoreMessage(score) {
  if (score >= 90) return '🌟 Outstanding! You\'re in the top tier of performers.';
  if (score >= 80) return '🎯 Excellent performance! Keep up this great work.';
  if (score >= 70) return '👍 Good job! A bit more effort will push you to excellence.';
  if (score >= 60) return '📈 Above average. Focus on the recommendations below.';
  if (score >= 50) return '⚠️ Just passing. Significant improvement needed.';
  return '🚨 Below passing threshold. Follow the action plan below urgently.';
}

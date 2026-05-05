/**
 * dashboard.js — Dashboard stats, charts, prediction history table
 */

document.addEventListener('DOMContentLoaded', async () => {
  await loadStats();
  await loadHistory();
});

// ── Load & render stats ───────────────────────────────────────
async function loadStats() {
  try {
    const stats = await apiGetStats();
    renderStatCards(stats);
    renderRecentChart(stats.recent_predictions || []);
    renderGradeChart(stats.grade_distribution || {});
    renderModelUsage(stats.model_usage || {});
  } catch (err) {
    console.warn('Stats unavailable:', err.message);
  }
}

function renderStatCards(stats) {
  setEl('stat-total',   stats.total_predictions);
  setEl('stat-avg',     stats.avg_predicted_score?.toFixed(1) + '%');
  setEl('stat-study',   stats.avg_study_hours?.toFixed(1) + ' hrs');
  setEl('stat-attend',  stats.avg_attendance?.toFixed(0) + '%');
}

function setEl(id, value) {
  const el = document.getElementById(id);
  if (el) {
    el.style.animation = 'countUp 0.5s ease forwards';
    el.textContent = value ?? '—';
  }
}

// ── Recent Score Trend Chart (mini line chart) ────────────────
function renderRecentChart(recent) {
  const canvas = document.getElementById('trend-chart');
  if (!canvas || !recent.length) return;

  const labels = recent.map((_, i) => `#${i + 1}`);
  const scores = recent.map(p => p.predicted_score);
  const colors = scores.map(s => scoreColor(s));

  new Chart(canvas, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Predicted Score',
        data: scores,
        borderColor: '#7c3aed',
        backgroundColor: 'rgba(124,58,237,0.12)',
        tension: 0.4,
        fill: true,
        pointBackgroundColor: colors,
        pointRadius: 5,
        pointHoverRadius: 7,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(15,15,46,0.95)',
          borderColor: 'rgba(255,255,255,0.1)',
          borderWidth: 1,
          callbacks: {
            label: ctx => ` ${ctx.parsed.y.toFixed(1)}%`,
          }
        }
      },
      scales: {
        y: {
          min: 0, max: 100,
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { color: '#64748b', font: { size: 11 } },
        },
        x: {
          grid: { display: false },
          ticks: { color: '#64748b', font: { size: 11 } },
        }
      }
    }
  });
}

// ── Grade Distribution Chart ──────────────────────────────────
function renderGradeChart(grades) {
  const canvas = document.getElementById('grade-chart');
  if (!canvas) return;

  const allGrades = ['A+', 'A', 'B', 'C', 'D', 'F'];
  const counts    = allGrades.map(g => grades[g] || 0);
  const palette   = ['#10b981', '#06b6d4', '#7c3aed', '#f59e0b', '#ef4444', '#6b7280'];

  new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: allGrades,
      datasets: [{
        data: counts,
        backgroundColor: palette.map(c => c + '33'),
        borderColor:     palette,
        borderWidth: 2,
        hoverOffset: 6,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '68%',
      plugins: {
        legend: {
          position: 'right',
          labels: {
            color: '#94a3b8',
            font: { size: 12 },
            padding: 12,
            usePointStyle: true,
          }
        },
        tooltip: {
          backgroundColor: 'rgba(15,15,46,0.95)',
          borderColor: 'rgba(255,255,255,0.1)',
          borderWidth: 1,
        }
      }
    }
  });
}

// ── Model usage display ───────────────────────────────────────
function renderModelUsage(usage) {
  const total = (usage.linear_regression || 0) + (usage.random_forest || 0);
  if (!total) return;

  const lrPct = Math.round(((usage.linear_regression || 0) / total) * 100);
  const rfPct = 100 - lrPct;

  const lrBar = document.getElementById('lr-bar');
  const rfBar = document.getElementById('rf-bar');
  const lrVal = document.getElementById('lr-pct');
  const rfVal = document.getElementById('rf-pct');

  if (lrBar) lrBar.style.width = lrPct + '%';
  if (rfBar) rfBar.style.width = rfPct + '%';
  if (lrVal) lrVal.textContent = lrPct + '%';
  if (rfVal) rfVal.textContent = rfPct + '%';
}

// ── History Table ─────────────────────────────────────────────
async function loadHistory() {
  const tbody = document.getElementById('history-tbody');
  const emptyState = document.getElementById('empty-history');
  if (!tbody) return;

  try {
    const data = await apiGetPredictions(1, 50);
    const preds = data.predictions || [];

    if (preds.length === 0) {
      tbody.innerHTML = '';
      if (emptyState) emptyState.classList.remove('hidden');
      return;
    }

    if (emptyState) emptyState.classList.add('hidden');

    tbody.innerHTML = preds.map(p => {
      const modelTag = p.model_used === 'random_forest'
        ? '<span class="model-tag rf">🌲 RF</span>'
        : '<span class="model-tag lr">📈 LR</span>';

      const gradeStyle = getGradeInlineStyle(p.performance_grade);

      return `
        <tr class="animate-fade-in">
          <td class="td-name">${escapeHtml(p.student_name || '—')}</td>
          <td>${p.study_hours?.toFixed(1)}</td>
          <td>${p.attendance?.toFixed(0)}%</td>
          <td>${p.sleep_hours?.toFixed(1)}</td>
          <td>${p.previous_score?.toFixed(0)}%</td>
          <td class="td-score">${p.predicted_score?.toFixed(1)}%</td>
          <td><span class="td-grade ${gradeClass(p.performance_grade)}" ${gradeStyle}>${p.performance_grade || '—'}</span></td>
          <td>${modelTag}</td>
          <td class="text-muted text-sm">${formatDate(p.created_at)}</td>
        </tr>`;
    }).join('');

  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="9" class="text-center text-muted" style="padding:2rem">Failed to load history: ${err.message}</td></tr>`;
  }
}

function getGradeInlineStyle(grade) {
  const colors = {
    'A+': '#10b981', 'A': '#06b6d4', 'B': '#7c3aed',
    'C': '#f59e0b',  'D': '#ef4444', 'F': '#6b7280'
  };
  const c = colors[grade] || '#6b7280';
  return `style="background:${c}22;color:${c};border:1px solid ${c}44"`;
}

function escapeHtml(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}

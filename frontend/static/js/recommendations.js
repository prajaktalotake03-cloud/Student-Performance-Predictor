/**
 * recommendations.js — Render AI recommendation cards
 */

function showRecommendations(tips) {
  const container = document.getElementById('recommendations-list');
  const section   = document.getElementById('recommendations-section');
  if (!container || !section) return;

  if (!tips || tips.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">💡</div>
        <p>No recommendations at this time.</p>
      </div>`;
    section.classList.remove('hidden');
    return;
  }

  container.innerHTML = tips.map((tip, i) => `
    <div class="recommendation-card priority-${tip.priority}" style="animation-delay:${i * 100}ms">
      <div class="rec-icon">${tip.icon}</div>
      <div class="rec-content">
        <div class="rec-title">${escapeHtml(tip.title)}</div>
        <div class="rec-desc">${escapeHtml(tip.description)}</div>
        <span class="priority-badge ${tip.priority}">${tip.priority}</span>
      </div>
    </div>
  `).join('');

  section.classList.remove('hidden');
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}

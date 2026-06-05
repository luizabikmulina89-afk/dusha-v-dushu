function buildMatchCard(match) {
  const card = document.createElement('div');
  card.className = 'match-card';

  const photoContent = match.photos && match.photos.length > 0
    ? `<img src="${match.photos[0]}" style="width:52px;height:52px;border-radius:50%;object-fit:cover;">`
    : `<div class="match-photo">👤</div>`;

  const lastMsg = match.last_message || 'Начните разговор!';
  const score = match.compatibility_score ? `${Math.round(match.compatibility_score)}%` : '';

  card.innerHTML = `
    ${photoContent}
    <div class="match-info">
      <div class="match-name">${match.pseudonym}, ${match.age}</div>
      <div class="match-meta">${match.city}${score ? ' · ' + score : ''}</div>
      <div class="match-last-msg">${lastMsg}</div>
    </div>
    <div class="match-arrow">→</div>
  `;

  card.onclick = () => {
    state.currentMatch = match;
    router.show('chat');
    initChat();
  };

  return card;
}

async function initMatches() {
  const telegramId = state.telegramId || tg.userId;
  const list = document.getElementById('matches-list');
  const empty = document.getElementById('matches-empty');
  const loading = document.getElementById('matches-loading');

  if (!list) return;

  list.innerHTML = '';
  if (loading) loading.classList.remove('hidden');
  if (empty) empty.classList.add('hidden');

  try {
    const data = await api.getMatches(telegramId);
    if (loading) loading.classList.add('hidden');

    if (!data.matches || data.matches.length === 0) {
      if (empty) empty.classList.remove('hidden');
      return;
    }

    data.matches.forEach(match => list.appendChild(buildMatchCard(match)));
  } catch (err) {
    if (loading) loading.classList.add('hidden');
    console.warn('Matches error:', err.message);
    if (empty) empty.classList.remove('hidden');
  }

  const btnBack = document.getElementById('btn-matches-back');
  if (btnBack && !btnBack._listenerAdded) {
    btnBack._listenerAdded = true;
    btnBack.onclick = () => router.show('feed');
  }
}

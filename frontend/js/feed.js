function showLimitBanner(list, limit) {
  const banner = document.createElement('div');
  banner.className = 'feed-limit-banner';
  banner.innerHTML = `
    <div class="feed-limit-text">
      <strong>Лимит ${limit} анкет/день исчерпан</strong><br>
      С Premium — безлимитные просмотры каждый день
    </div>
    <button class="btn-get-premium" id="btn-go-premium">Premium ⭐</button>
  `;
  list.appendChild(banner);
  const btn = banner.querySelector('#btn-go-premium');
  if (btn) btn.onclick = () => showPremiumScreen();
}

function getCompatColor(pct) {
  if (pct >= 80) return 'green';
  if (pct >= 65) return 'yellow';
  return 'orange';
}

function buildFeedCard(candidate) {
  const color = getCompatColor(candidate.compatibility_score);
  const card = document.createElement('div');
  card.className = 'feed-card';
  card.dataset.userId = candidate.user_id;

  const photoContent = candidate.photos && candidate.photos.length > 0
    ? `<img src="${candidate.photos[0]}" alt="фото" class="feed-card-photo">`
    : `<div class="feed-card-photo">👤</div>`;

  const tags = [];
  if (candidate.zodiac_sign) tags.push(`♌ ${candidate.zodiac_sign}`);
  if (candidate.hd_type) tags.push(`⚡ ${candidate.hd_type}`);

  const pct = candidate.compatibility_score;
  const barWidth = Math.min(pct, 100);

  card.innerHTML = `
    ${photoContent}
    <div class="feed-card-info">
      <div class="feed-card-name">${candidate.pseudonym}, ${candidate.age}</div>
      <div class="feed-card-meta">${candidate.city}</div>
      <div class="feed-card-tags">
        ${tags.map(t => `<span class="feed-tag">${t}</span>`).join('')}
      </div>
      <div class="compat-bar-mini">
        <div class="compat-bar-track">
          <div class="compat-bar-fill ${color}" style="width:${barWidth}%"></div>
        </div>
        <span class="compat-pct ${color}">${pct}%</span>
      </div>
    </div>
  `;

  card.addEventListener('click', () => {
    state.currentCandidate = candidate;
    router.show('candidate');
    if (typeof initCandidateProfile === 'function') initCandidateProfile();
  });

  return card;
}

async function initFeed() {
  const telegramId = state.telegramId || tg.userId;
  const list = document.getElementById('feed-list');
  const empty = document.getElementById('feed-empty');
  const loading = document.getElementById('feed-loading');

  if (!list) return;

  // Навешиваем обработчики сразу — до любых return
  const btnInvite = document.getElementById('btn-invite');
  if (btnInvite && !btnInvite._listenerAdded) {
    btnInvite._listenerAdded = true;
    btnInvite.addEventListener('click', () => {
      const userId = state.telegramId || tg.userId;
      const inviteLink = `https://t.me/DushaVDushuApp_bot?start=ref_${userId}`;
      const text = 'Заходи в «Душа в душу» — найдём твоего человека по нумерологии и астрологии! 💫';
      const shareUrl = `https://t.me/share/url?url=${encodeURIComponent(inviteLink)}&text=${encodeURIComponent(text)}`;
      if (tg.webapp && tg.webapp.openTelegramLink) {
        tg.webapp.openTelegramLink(shareUrl);
      } else {
        window.open(shareUrl, '_blank');
      }
    });
  }

  const btnProfile = document.getElementById('btn-my-profile');
  if (btnProfile && !btnProfile._listenerAdded) {
    btnProfile._listenerAdded = true;
    btnProfile.addEventListener('click', () => {
      alert('Профиль — в следующем обновлении!');
    });
  }

  const btnMatchesNav = document.getElementById('btn-matches-nav');
  if (btnMatchesNav && !btnMatchesNav._listenerAdded) {
    btnMatchesNav._listenerAdded = true;
    btnMatchesNav.addEventListener('click', () => {
      router.show('matches');
      initMatches();
    });
  }

  list.innerHTML = '';
  if (loading) loading.classList.remove('hidden');
  if (empty) empty.classList.add('hidden');

  try {
    const data = await api.getFeed(telegramId);
    if (loading) loading.classList.add('hidden');

    if (data.limit_reached) {
      showLimitBanner(list, data.daily_limit);
      return;
    }

    if (!data.candidates || data.candidates.length === 0) {
      if (empty) empty.classList.remove('hidden');
      return;
    }

    data.candidates.forEach(candidate => {
      list.appendChild(buildFeedCard(candidate));
    });

  } catch (err) {
    if (loading) loading.classList.add('hidden');
    console.warn('Feed error:', err.message);

    const mockCandidates = [
      { user_id: 1, pseudonym: 'Анна', age: 29, city: 'Москва', photos: [], compatibility_score: 87, zodiac_sign: 'Лев', hd_type: 'Генератор' },
      { user_id: 2, pseudonym: 'Мария', age: 31, city: 'Москва', photos: [], compatibility_score: 74, zodiac_sign: 'Рыбы', hd_type: 'Проектор' },
      { user_id: 3, pseudonym: 'Елена', age: 27, city: 'СПб', photos: [], compatibility_score: 62, zodiac_sign: 'Скорпион', hd_type: 'Манифестор' },
    ];
    mockCandidates.forEach(c => list.appendChild(buildFeedCard(c)));
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (state.isRegistered) {
    initFeed();
  }
});

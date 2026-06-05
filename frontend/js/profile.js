const SYSTEM_LABELS = {
  numerology:    '✨ Нумерология',
  astrology:     '♌ Астрология',
  human_design:  '⚡ Human Design',
  matrix_fate:   '🔮 Матрица судьбы',
  psychotype:    '🧠 Психотип',
  enneagram:     '🌀 Эннеаграмма',
  attachment:    '💞 Тип привязанности',
  love_language: '❤️ Язык любви',
  values:        '🎯 Ценности',
};

function buildCompatRow(label, pct) {
  const color = pct >= 80 ? 'green' : pct >= 65 ? 'yellow' : 'orange';
  const row = document.createElement('div');
  row.className = 'compat-row';
  row.innerHTML = `
    <span class="compat-system-name">${label}</span>
    <div class="compat-bar-track">
      <div class="compat-bar-fill ${color}" style="width:${pct}%"></div>
    </div>
    <span class="compat-row-pct compat-pct ${color}">${pct}%</span>
  `;
  return row;
}

function initCandidateProfile() {
  const candidate = state.currentCandidate;
  if (!candidate) return;

  const nameEl = document.getElementById('candidate-name');
  const locEl = document.getElementById('candidate-location');
  const aboutEl = document.getElementById('candidate-about');
  const badge = document.getElementById('candidate-score-badge');
  const photosEl = document.getElementById('candidate-photos');
  const breakdownEl = document.getElementById('compat-breakdown');

  if (nameEl) nameEl.textContent = `${candidate.pseudonym}, ${candidate.age}`;
  if (locEl) locEl.textContent = candidate.city;
  if (aboutEl) aboutEl.textContent = candidate.about_me || '';
  if (badge) badge.textContent = `${candidate.compatibility_score}%`;

  if (photosEl) {
    if (candidate.photos && candidate.photos.length > 0) {
      photosEl.innerHTML = `<img src="${candidate.photos[0]}" alt="фото">`;
    } else {
      photosEl.innerHTML = '👤';
    }
  }

  if (breakdownEl) {
    breakdownEl.innerHTML = '';
    const breakdown = candidate.compatibility_breakdown || {};
    const systemsUsed = candidate.systems_used || 0;

    if (Object.keys(breakdown).length === 0) {
      breakdownEl.innerHTML = `<p style="color:#888;font-size:13px;">Разбивка по системам доступна после заполнения профиля обоими пользователями</p>`;
    } else {
      Object.entries(breakdown).forEach(([key, pct]) => {
        const label = SYSTEM_LABELS[key] || key;
        breakdownEl.appendChild(buildCompatRow(label, pct));
      });

      if (systemsUsed < 9) {
        const note = document.createElement('div');
        note.style.cssText = 'font-size:12px;color:#999;margin-top:8px;';
        note.textContent = `Совместимость по ${systemsUsed} из 9 систем`;
        breakdownEl.appendChild(note);
      }
    }
  }

  const btnLike = document.getElementById('btn-like');
  const btnPass = document.getElementById('btn-pass');
  const btnSuper = document.getElementById('btn-super');

  if (btnLike) {
    btnLike.onclick = async () => {
      tg.hapticSuccess();
      try {
        const result = await api.sendLike(state.telegramId || tg.userId, candidate.user_id, false);
        if (result.matched) {
          tg.hapticSuccess();
          state.currentMatch = {
            match_id: result.match_id,
            pseudonym: candidate.pseudonym,
            age: candidate.age,
            city: candidate.city,
            photos: candidate.photos || [],
            compatibility_score: candidate.compatibility_score,
          };
          tg.showAlert(
            `💫 Космическое совпадение с ${candidate.pseudonym}!\n\n` +
            `Совместимость: ${candidate.compatibility_score}%\n\n` +
            `Нажмите 💫 в ленте, чтобы начать общение!`
          );
        } else {
          tg.showAlert('Лайк отправлен! ♥');
        }
      } catch (err) {
        tg.showAlert('Лайк отправлен! ♥');
      }
      router.show('feed');
    };
  }

  if (btnPass) {
    btnPass.onclick = () => {
      tg.hapticLight();
      router.show('feed');
    };
  }

  if (btnSuper) {
    btnSuper.onclick = async () => {
      tg.hapticSuccess();
      try {
        await api.sendLike(state.telegramId || tg.userId, candidate.user_id, true);
        tg.showAlert(`⭐ Суперлайк отправлен!\n\n${candidate.pseudonym} увидит, что ты особо выделил(а) её профиль`);
      } catch (err) {
        tg.showAlert('⭐ Суперлайк отправлен!');
      }
      router.show('feed');
    };
  }

  const btnBack = document.getElementById('btn-candidate-back');
  if (btnBack) {
    btnBack.onclick = () => router.show('feed');
  }
}

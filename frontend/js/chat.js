function formatTime(isoStr) {
  const d = new Date(isoStr);
  return d.toLocaleTimeString('ru', { hour: '2-digit', minute: '2-digit' });
}

function buildBubble(msg) {
  const wrap = document.createElement('div');
  wrap.style.display = 'flex';
  wrap.style.flexDirection = 'column';
  wrap.style.alignItems = msg.is_mine ? 'flex-end' : 'flex-start';

  const bubble = document.createElement('div');
  bubble.className = `chat-bubble ${msg.is_mine ? 'mine' : 'theirs'}`;
  bubble.textContent = msg.text;

  const time = document.createElement('div');
  time.className = 'chat-bubble-time';
  time.textContent = formatTime(msg.created_at);
  bubble.appendChild(time);

  wrap.appendChild(bubble);
  return wrap;
}

async function loadMessages(matchId) {
  const telegramId = state.telegramId || tg.userId;
  const container = document.getElementById('chat-messages');
  if (!container) return;

  try {
    const data = await api.getMessages(matchId, telegramId);
    container.innerHTML = '';

    if (data.messages.length === 0) {
      container.innerHTML = '<div class="chat-empty">Напишите первое сообщение ✨</div>';
    } else {
      data.messages.forEach(msg => container.appendChild(buildBubble(msg)));
      container.scrollTop = container.scrollHeight;
    }

    if (data.match_expires_at) {
      const expiry = new Date(data.match_expires_at);
      const daysLeft = Math.ceil((expiry - Date.now()) / 86400000);
      const note = document.getElementById('chat-expiry-note');
      if (note && daysLeft <= 3) {
        note.textContent = `⚠️ Чат исчезнет через ${daysLeft} дн. — напишите что-нибудь`;
        note.classList.remove('hidden');
      }
    }
  } catch (err) {
    container.innerHTML = '<div class="chat-empty">Не удалось загрузить сообщения</div>';
  }
}

async function sendChatMessage(matchId) {
  const input = document.getElementById('chat-input');
  const text = input.value.trim();
  if (!text) return;

  input.value = '';
  tg.hapticLight();

  const telegramId = state.telegramId || tg.userId;
  try {
    await api.sendMessage(matchId, telegramId, text);
    await loadMessages(matchId);
  } catch (err) {
    tg.showAlert('Не удалось отправить сообщение');
    input.value = text;
  }
}

function initChat() {
  const match = state.currentMatch;
  if (!match) return;

  const nameEl = document.getElementById('chat-partner-name');
  const badgeEl = document.getElementById('chat-compat-badge');
  if (nameEl) nameEl.textContent = match.pseudonym;
  if (badgeEl && match.compatibility_score) {
    badgeEl.textContent = `${Math.round(match.compatibility_score)}%`;
  }

  loadMessages(match.match_id);

  const sendBtn = document.getElementById('btn-send-message');
  const input = document.getElementById('chat-input');

  if (sendBtn) sendBtn.onclick = () => sendChatMessage(match.match_id);
  if (input) {
    input.onkeydown = (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendChatMessage(match.match_id);
      }
    };
  }

  const btnBack = document.getElementById('btn-chat-back');
  if (btnBack) btnBack.onclick = () => router.show('matches');
}

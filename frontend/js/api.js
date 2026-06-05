// Локально (открыть напрямую в браузере): обращаемся к localhost:8000
// На Railway (фронтенд раздаёт сам FastAPI): используем тот же origin
const API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://127.0.0.1:8000'
  : window.location.origin;

const api = {
  async request(method, path, body) {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(`${API_BASE}${path}`, opts);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    return res.json();
  },

  register(data) {
    return this.request('POST', '/users/register', data);
  },

  updateBirthData(telegramId, data) {
    return this.request('POST', `/users/${telegramId}/birth-data`, data);
  },

  updateHardFilters(telegramId, data) {
    return this.request('POST', `/users/${telegramId}/hard-filters`, data);
  },

  submitTest(telegramId, testType, answers) {
    return this.request('POST', `/users/${telegramId}/test`, {
      test_type: testType,
      answers,
    });
  },

  getFeed(telegramId) {
    return this.request('GET', `/feed/${telegramId}`);
  },

  sendLike(telegramId, targetUserId, isSuper = false) {
    return this.request('POST', `/likes/${telegramId}/like/${targetUserId}?is_super=${isSuper}`);
  },

  getMatches(telegramId) {
    return this.request('GET', `/likes/${telegramId}/matches`);
  },

  getMessages(matchId, telegramId) {
    return this.request('GET', `/chat/${matchId}?telegram_id=${telegramId}`);
  },

  sendMessage(matchId, telegramId, text) {
    return this.request('POST', `/chat/${matchId}/send?telegram_id=${telegramId}`, { text });
  },

  createInvoice(telegramId) {
    return this.request('POST', `/payments/create-invoice/${telegramId}`);
  },
};

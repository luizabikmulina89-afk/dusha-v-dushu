const API_BASE = 'http://127.0.0.1:8000';

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
};

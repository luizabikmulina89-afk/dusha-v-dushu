const state = {
  _data: JSON.parse(localStorage.getItem('dusha_state') || '{}'),

  get(key) {
    return this._data[key];
  },

  set(key, value) {
    this._data[key] = value;
    localStorage.setItem('dusha_state', JSON.stringify(this._data));
  },

  reg: {
    get step1() { return state.get('reg_step1') || {}; },
    set step1(v) { state.set('reg_step1', v); },
    get step2() { return state.get('reg_step2') || {}; },
    set step2(v) { state.set('reg_step2', v); },
    get step3() { return state.get('reg_step3') || {}; },
    set step3(v) { state.set('reg_step3', v); },
    get step4() { return state.get('reg_step4') || {}; },
    set step4(v) { state.set('reg_step4', v); },
  },

  get isRegistered() { return !!this.get('telegram_id'); },
  get telegramId() { return this.get('telegram_id'); },
  set telegramId(v) { this.set('telegram_id', v); },

  get onboardingDone() { return !!this.get('onboarding_done'); },
  set onboardingDone(v) { this.set('onboarding_done', v); },

  get currentCandidate() { return this.get('current_candidate'); },
  set currentCandidate(v) { this.set('current_candidate', v); },

  showError(msg) {
    alert(msg);
  },
};

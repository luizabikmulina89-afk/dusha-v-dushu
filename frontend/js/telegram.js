const tg = {
  get webapp() {
    return window.Telegram?.WebApp || null;
  },

  get user() {
    const u = this.webapp?.initDataUnsafe?.user;
    if (u) return u;
    return { id: 99999, first_name: 'Тест', username: 'testuser' };
  },

  get userId() {
    return this.user.id;
  },

  get firstName() {
    return this.user.first_name || 'друг';
  },

  init() {
    if (this.webapp) {
      this.webapp.ready();
      this.webapp.expand();
    }
  },

  close() {
    this.webapp?.close();
  },

  showAlert(msg) {
    if (this.webapp) {
      this.webapp.showAlert(msg);
    } else {
      alert(msg);
    }
  },

  hapticLight() {
    this.webapp?.HapticFeedback?.impactOccurred('light');
  },

  hapticSuccess() {
    this.webapp?.HapticFeedback?.notificationOccurred('success');
  },
};

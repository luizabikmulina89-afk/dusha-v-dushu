const router = {
  current: null,

  show(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
    const screen = document.getElementById(`screen-${screenId}`);
    if (!screen) {
      console.error(`Экран screen-${screenId} не найден`);
      return;
    }
    screen.classList.remove('hidden');
    this.current = screenId;
    window.scrollTo(0, 0);
  },

  init() {
    tg.init();

    if (state.isRegistered) {
      this.show('feed');
    } else if (state.onboardingDone) {
      this.show('reg-1');
    } else {
      this.show('onboarding-1');
    }
  },
};

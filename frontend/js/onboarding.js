function initOnboarding() {
  document.getElementById('btn-onb1-next').addEventListener('click', () => {
    tg.hapticLight();
    router.show('onboarding-2');
  });

  document.getElementById('btn-onb2-next').addEventListener('click', () => {
    tg.hapticLight();
    router.show('onboarding-3');
  });

  document.getElementById('btn-onb3-start').addEventListener('click', () => {
    tg.hapticSuccess();
    state.onboardingDone = true;
    router.show('reg-1');
  });

  const counter = document.getElementById('couples-counter');
  if (counter) counter.textContent = '1 247 пар нашли друг друга';

  document.getElementById('privacy-link').addEventListener('click', (e) => {
    e.preventDefault();
    tg.showAlert('Политика конфиденциальности: мы собираем только данные, необходимые для подбора партнёра. Все данные хранятся на серверах в России согласно 152-ФЗ. Вы можете запросить удаление данных в любой момент через профиль.');
  });
}

document.addEventListener('DOMContentLoaded', () => {
  router.init();
  initOnboarding();
});

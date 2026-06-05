function initPremium() {
  const btnBack = document.getElementById('btn-premium-back');
  if (btnBack) btnBack.onclick = () => router.show('feed');

  const btnBuy = document.getElementById('btn-buy-premium');
  if (btnBuy) {
    btnBuy.onclick = async () => {
      tg.hapticSuccess();
      const telegramId = state.telegramId || tg.userId;
      try {
        const data = await api.createInvoice(telegramId);
        if (!data.invoice_link) throw new Error('no link');

        // Открываем Telegram-инвойс внутри mini app
        if (typeof Telegram !== 'undefined' && Telegram.WebApp && Telegram.WebApp.openInvoice) {
          Telegram.WebApp.openInvoice(data.invoice_link, (status) => {
            if (status === 'paid') {
              tg.showAlert('✨ Premium активирован на 30 дней! Наслаждайся безлимитным поиском.');
              router.show('feed');
              initFeed();
            } else if (status === 'failed') {
              tg.showAlert('Оплата не прошла. Попробуй ещё раз.');
            }
          });
        } else {
          // Фоллбэк — открываем ссылку
          window.open(data.invoice_link, '_blank');
        }
      } catch (err) {
        tg.showAlert('Не удалось создать счёт. Попробуй позже.');
      }
    };
  }
}

function showPremiumScreen() {
  router.show('premium');
  initPremium();
}

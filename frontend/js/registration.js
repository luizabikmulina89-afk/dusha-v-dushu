// === Функции валидации ===

function validateStep1(data) {
  return !!(data.name && data.name.trim().length >= 2);
}

function validateBirthDate(str) {
  if (!str) return false;
  const parts = str.split('.');
  if (parts.length !== 3) return false;
  const [d, m, y] = parts.map(Number);
  if (!d || !m || !y) return false;
  if (d < 1 || d > 31 || m < 1 || m > 12 || y < 1900 || y > 2010) return false;
  return true;
}

function validateAge(age) {
  return age >= 18 && age <= 99;
}

// === UI-утилиты ===

function setupRadioGroup(groupId, onSelect) {
  const group = document.getElementById(groupId);
  if (!group) return;
  group.querySelectorAll('.radio-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      group.querySelectorAll('.radio-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      if (onSelect) onSelect(btn.dataset.value);
    });
  });
}

function getRadioValue(groupId) {
  const selected = document.querySelector(`#${groupId} .radio-btn.selected`);
  return selected ? selected.dataset.value : null;
}

function showFieldError(inputEl, msg) {
  inputEl.style.borderColor = '#e53935';
  const existing = inputEl.nextElementSibling;
  if (existing && existing.classList.contains('field-error')) existing.remove();
  const err = document.createElement('div');
  err.className = 'field-error';
  err.style.cssText = 'color:#e53935;font-size:12px;margin-top:-6px;';
  err.textContent = msg;
  inputEl.after(err);
}

function clearFieldError(inputEl) {
  inputEl.style.borderColor = '';
  const next = inputEl.nextElementSibling;
  if (next && next.classList.contains('field-error')) next.remove();
}

// === Счётчик символов «о себе» ===
function initCharCounter() {
  const textarea = document.getElementById('reg1-about');
  const counter = document.getElementById('reg1-about-count');
  if (!textarea || !counter) return;
  textarea.addEventListener('input', () => {
    counter.textContent = textarea.value.length;
  });
}

// === Загрузка фото ===
function initPhotoUpload() {
  const area = document.getElementById('photo-upload-area');
  const input = document.getElementById('photo-input');
  const placeholder = document.getElementById('photo-placeholder');
  const grid = document.getElementById('photos-grid');
  const photos = [];

  if (!area || !input) return photos;

  area.addEventListener('click', (e) => {
    if (e.target !== input) input.click();
  });

  input.addEventListener('change', () => {
    const files = Array.from(input.files).slice(0, 5 - photos.length);
    files.forEach(file => {
      const reader = new FileReader();
      reader.onload = (e) => {
        photos.push(e.target.result);
        if (placeholder) placeholder.style.display = 'none';
        const img = document.createElement('img');
        img.src = e.target.result;
        img.className = 'photo-thumb';
        grid.appendChild(img);
      };
      reader.readAsDataURL(file);
    });
  });

  return photos;
}

// === Шаг 1: Фото + имя + о себе ===
function initStep1() {
  initCharCounter();
  const photos = initPhotoUpload();

  document.getElementById('btn-reg1-next').addEventListener('click', async () => {
    const nameEl = document.getElementById('reg1-name');
    const aboutEl = document.getElementById('reg1-about');
    const name = nameEl.value.trim();
    const about = aboutEl.value.trim();

    clearFieldError(nameEl);

    if (!validateStep1({ name })) {
      showFieldError(nameEl, 'Введи псевдоним — минимум 2 символа');
      return;
    }

    state.reg.step1 = { name, about, photos: photos.slice(0, 5) };
    tg.hapticLight();
    router.show('reg-2');
  });
}

// === Шаг 2: Пол, ориентация, возраст, город ===
function initStep2() {
  setupRadioGroup('reg2-gender');
  setupRadioGroup('reg2-orientation');
  setupRadioGroup('reg2-pref-gender');
  setupRadioGroup('reg2-relation-type');

  const saved = state.reg.step2;
  if (saved.gender) {
    const btn = document.querySelector(`#reg2-gender [data-value="${saved.gender}"]`);
    if (btn) btn.classList.add('selected');
  }

  document.getElementById('btn-reg2-back').addEventListener('click', () => router.show('reg-1'));

  document.getElementById('btn-reg2-next').addEventListener('click', () => {
    const ageEl = document.getElementById('reg2-age');
    const cityEl = document.getElementById('reg2-city');
    const gender = getRadioValue('reg2-gender');
    const orientation = getRadioValue('reg2-orientation');
    const age = parseInt(ageEl.value);
    const city = cityEl.value.trim();
    const prefGender = getRadioValue('reg2-pref-gender');
    const ageMin = parseInt(document.getElementById('reg2-age-min').value) || 18;
    const ageMax = parseInt(document.getElementById('reg2-age-max').value) || 60;
    const relationType = getRadioValue('reg2-relation-type');

    clearFieldError(ageEl);
    clearFieldError(cityEl);

    if (!gender) { tg.showAlert('Выбери пол'); return; }
    if (!orientation) { tg.showAlert('Выбери ориентацию'); return; }
    if (!validateAge(age)) {
      showFieldError(ageEl, 'Приложение только для совершеннолетних (18+)');
      return;
    }
    if (!city) { showFieldError(cityEl, 'Укажи город проживания'); return; }
    if (!prefGender) { tg.showAlert('Укажи, кого ищешь'); return; }
    if (!relationType) { tg.showAlert('Выбери тип отношений'); return; }

    state.reg.step2 = {
      gender, orientation, age, city,
      pref_gender: prefGender,
      pref_age_min: ageMin,
      pref_age_max: ageMax,
      pref_relation_type: relationType,
    };
    tg.hapticLight();
    router.show('reg-3');
  });
}

// === Шаг 3: Дата рождения ===
function initStep3() {
  const birthdateEl = document.getElementById('reg3-birthdate');
  const resultsEl = document.getElementById('reg3-results');
  const chipsEl = document.getElementById('reg3-chips');

  // Авто-форматирование ДД.ММ.ГГГГ при вводе
  birthdateEl.addEventListener('input', (e) => {
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 2) v = v.slice(0, 2) + '.' + v.slice(2);
    if (v.length > 5) v = v.slice(0, 5) + '.' + v.slice(5);
    e.target.value = v.slice(0, 10);
  });

  document.getElementById('btn-reg3-back').addEventListener('click', () => router.show('reg-2'));

  document.getElementById('btn-reg3-next').addEventListener('click', async () => {
    const birthDate = birthdateEl.value.trim();
    clearFieldError(birthdateEl);

    if (!validateBirthDate(birthDate)) {
      showFieldError(birthdateEl, 'Введи дату в формате ДД.ММ.ГГГГ (например: 15.03.1990)');
      return;
    }

    const birthTime = document.getElementById('reg3-birthtime').value.trim() || null;
    const birthCity = document.getElementById('reg3-birthcity').value.trim() || null;

    state.reg.step3 = { birth_date: birthDate, birth_time: birthTime, birth_city: birthCity };

    try {
      const telegramId = tg.userId;

      if (!state.isRegistered) {
        const s1 = state.reg.step1;
        const s2 = state.reg.step2;
        await api.register({
          telegram_id: telegramId,
          pseudonym: s1.name,
          about_me: s1.about || '',
          gender: s2.gender,
          orientation: s2.orientation,
          age: s2.age,
          city: s2.city,
          pref_gender: s2.pref_gender,
          pref_age_min: s2.pref_age_min,
          pref_age_max: s2.pref_age_max,
          pref_relation_type: s2.pref_relation_type,
        });
        state.telegramId = telegramId;
      }

      const result = await api.updateBirthData(telegramId, {
        birth_date: birthDate,
        birth_time: birthTime,
        birth_city: birthCity,
      });

      chipsEl.innerHTML = '';
      if (result.life_path) {
        chipsEl.innerHTML += `<div class="calc-chip">✨ Число пути: ${result.life_path}</div>`;
      }
      if (result.zodiac) {
        chipsEl.innerHTML += `<div class="calc-chip">♌ ${result.zodiac}</div>`;
      }
      if (result.hd_type) {
        chipsEl.innerHTML += `<div class="calc-chip">⚡ HD: ${result.hd_type}</div>`;
      }
      resultsEl.classList.remove('hidden');

      setTimeout(() => {
        tg.hapticSuccess();
        router.show('reg-4');
      }, 1500);

    } catch (err) {
      console.warn('Backend error:', err.message);
      tg.hapticLight();
      router.show('reg-4');
    }
  });
}

// === Шаг 4: Жёсткие фильтры ===
function initStep4() {
  setupRadioGroup('reg4-children');
  setupRadioGroup('reg4-marriage');
  setupRadioGroup('reg4-religion-own');
  setupRadioGroup('reg4-religion-partner');
  setupRadioGroup('reg4-smoking');
  setupRadioGroup('reg4-alcohol');

  document.getElementById('btn-reg4-back').addEventListener('click', () => router.show('reg-3'));

  document.getElementById('btn-reg4-finish').addEventListener('click', async () => {
    const children = getRadioValue('reg4-children');
    const marriage = getRadioValue('reg4-marriage');
    const religionOwn = getRadioValue('reg4-religion-own');
    const religionPartner = getRadioValue('reg4-religion-partner');
    const smoking = getRadioValue('reg4-smoking');
    const alcohol = getRadioValue('reg4-alcohol');

    if (!children) { tg.showAlert('Укажи отношение к детям'); return; }
    if (!marriage) { tg.showAlert('Укажи отношение к браку'); return; }
    if (!religionOwn) { tg.showAlert('Укажи свою религию'); return; }
    if (!religionPartner) { tg.showAlert('Укажи важна ли вера партнёра'); return; }
    if (!smoking) { tg.showAlert('Укажи отношение к курению'); return; }
    if (!alcohol) { tg.showAlert('Укажи отношение к алкоголю'); return; }

    state.reg.step4 = { children, marriage, religionOwn, religionPartner, smoking, alcohol };

    try {
      const telegramId = state.telegramId || tg.userId;
      await api.updateHardFilters(telegramId, {
        wants_children: children,
        wants_marriage: marriage,
        religion_own: religionOwn,
        religion_partner: religionPartner,
        smoking,
        alcohol,
      });
    } catch (err) {
      console.warn('Hard filters error:', err.message);
    }

    tg.hapticSuccess();
    router.show('loading');

    setTimeout(() => {
      router.show('feed');
      if (typeof initFeed === 'function') initFeed();
    }, 1500);
  });
}

// === Инициализация всех шагов ===
function initRegistration() {
  initStep1();
  initStep2();
  initStep3();
  initStep4();
}

document.addEventListener('DOMContentLoaded', initRegistration);

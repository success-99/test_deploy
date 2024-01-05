let timer;

function resetTimer() {
  clearTimeout(timer);
  timer = setTimeout(logoutUser, 10000); // 30 sekunddan so'ng avtomatik ravishda logout
}

function logoutUser() {
  window.location.href = '/out-clear-cookie'; // logout url manziliga o'tkazish
}

// Foydalanuvchi faol harakat qilganda taymer resetlanadi
document.addEventListener('mousemove', resetTimer);
document.addEventListener('keypress', resetTimer);

// Sahifani yuklagan paytda taymer ishga tushadi
resetTimer();

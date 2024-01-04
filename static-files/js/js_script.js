//let idleTime = 0;
//const idleInterval = setInterval(timerIncrement, 10000); // Har bir daqiqada tekshirish
//
//function timerIncrement() {
//  idleTime += 1;
//  if (idleTime > 1) { // 60 daqiqa nofaol bo'lganda
//    logoutUser(); // Foydalanuvchini logout qilish
//  }
//}
//
//// Foydalanuvchi logout qilish funksiyasi
//function logoutUser() {
//  // Bu yerda logout amalini bajarish mumkin, masalan, logout URL ga yo'naltirish
//  window.location.href = '/logout'; // '/logout' ni o'z logout URLingiz bilan almashtiring
//}
//
//// Foydalanuvchi faollik qilishi bo'yicha tekshirish vaqtni qayta o'rnatish
//document.addEventListener('mousemove', function() {
//  idleTime = 0;
//});
//
//document.addEventListener('keypress', function() {
//  idleTime = 0;
//});


let timer;

function resetTimer() {
  clearTimeout(timer);
  timer = setTimeout(logoutUser, 1800000);
}

function logoutUser() {
  window.location.href = '/out-clear-cookie'; // logout url manziliga o'tkazish
}

// Foydalanuvchi faol harakat qilganda taymer resetlanadi
document.addEventListener('mousemove', resetTimer);
document.addEventListener('keypress', resetTimer);

// Sahifani yuklagan paytda taymer ishga tushadi
resetTimer();

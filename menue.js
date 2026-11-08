// Menue-Knopf fuer schmale Bildschirme: Die Kopfzeile bleibt eine Zeile, die Links
// klappen darunter auf. Gilt fuer alle Seiten der Webseite.
(function () {
  var kopf = document.querySelector('.site-header');
  var knopf = kopf && kopf.querySelector('.menue-knopf');
  if (!kopf || !knopf) return;
  function setzen(auf) {
    kopf.classList.toggle('offen', auf);
    knopf.setAttribute('aria-expanded', auf ? 'true' : 'false');
    knopf.setAttribute('aria-label', auf ? 'Menü schließen' : 'Menü öffnen');
  }
  knopf.addEventListener('click', function (e) { e.stopPropagation(); setzen(!kopf.classList.contains('offen')); });
  document.addEventListener('click', function (e) { if (!kopf.contains(e.target)) setzen(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setzen(false); });
  [].forEach.call(kopf.querySelectorAll('.nav-links a'), function (a) {
    a.addEventListener('click', function () { setzen(false); });
  });
})();

// weakness.js - small behavior: animate bars and filter strong multipliers
document.addEventListener('DOMContentLoaded', () => {
  // animate all bars: each .weak-bar has CSS variable --target set inline (percentage)
  document.querySelectorAll('.weak-bar').forEach((el) => {
    const target = getComputedStyle(el).getPropertyValue('--target').trim();
    if (target) {
      // small delay for stagger
      setTimeout(() => { el.style.width = target; }, 120);
    }
  });

  const filterStrong = document.getElementById('filter-strong');
  const filterAll = document.getElementById('filter-all');

  function setActive(btn) {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }

  filterStrong && filterStrong.addEventListener('click', () => {
    setActive(filterStrong);
    document.querySelectorAll('.weak-card').forEach(card => {
      const mult = parseFloat(card.dataset.mult) || 1;
      card.style.display = (mult >= 2) ? '' : 'none';
    });
  });

  filterAll && filterAll.addEventListener('click', () => {
    setActive(filterAll);
    document.querySelectorAll('.weak-card').forEach(card => card.style.display = '');
  });
});

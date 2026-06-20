
document.addEventListener('DOMContentLoaded', function () {
const modal = new bootstrap.Modal(document.getElementById('forcedModal'));
modal.show();
});

document.addEventListener('DOMContentLoaded', function () {
  const modal = new bootstrap.Modal(document.getElementById('forcedModal'));
  modal.show();

  document.querySelectorAll('details[data-character-id]').forEach(function (detail) {
    detail.addEventListener('click', function () {
      // Remove highlight from all
      document.querySelectorAll('details[data-character-id]').forEach(d => d.classList.remove('selected-character'));
      // Highlight clicked
      detail.classList.add('selected-character');
      // Update hidden input and enable button
      document.getElementById('selectedCharacterId').value = detail.dataset.characterId;
      document.getElementById('continueBtn').disabled = false;
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const modalEl = document.getElementById('forcedModal');
  if (!modalEl) return;  // character already selected, modal not in DOM

  const modal = new bootstrap.Modal(modalEl);
  modal.show();
  // ...rest of click handlers
});
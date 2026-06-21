
document.addEventListener('DOMContentLoaded', function () {
  // --- Character selection modal ---
  const forcedModalEl = document.getElementById('forcedModal');
  if (forcedModalEl) {
    const forcedModal = new bootstrap.Modal(forcedModalEl);
    forcedModal.show();

    document.querySelectorAll('details[data-character-id]').forEach(function (detail) {
      detail.addEventListener('click', function () {
        document.querySelectorAll('details[data-character-id]').forEach(d => d.classList.remove('selected-character'));
        detail.classList.add('selected-character');
        document.getElementById('selectedCharacterId').value = detail.dataset.characterId;
        document.getElementById('continueBtn').disabled = false;
      });
    });
  }

  // --- Battle result modal ---
  const battleForm = document.getElementById('battleForm');
  if (battleForm) {
    let lastResult = null;
    const resultModalEl = document.getElementById('battleResultModal');
    const resultModal = new bootstrap.Modal(resultModalEl);
    const resultTitle = document.getElementById('battleResultTitle');
    const resultMessage = document.getElementById('battleResultMessage');
    const resultClose = document.getElementById('battleResultClose');

    const messages = {
      character_win: { title: 'Victory!',         text: 'You defeated the enemy and gained XP!' },
      draw:          { title: 'Draw',              text: 'Neither side won. A new enemy approaches...' },
      game_over:     { title: 'Defeated',          text: 'Your character was defeated. Game over.' },
      win:           { title: 'Gauntlet Clear!',   text: 'You completed all waves!' },
      boss_awakened: { title: 'The Boss Awakens!', text: 'The boss has transformed — prepare yourself!' },
    };

    battleForm.addEventListener('submit', function (e) {
      e.preventDefault();
      fetch('/api/battle', {
        method: 'POST',
        body: new FormData(battleForm),
      })
      .then(r => r.json())
      .then(data => {
        const msg = messages[data.result] || { title: 'Result', text: data.result };
        resultTitle.textContent = msg.title;
        resultMessage.textContent = msg.text;

        const grid = document.getElementById('attributeGrid');
        grid.innerHTML = '';
        const enemy = data.fought_enemy;

        for (const [attr, winner] of Object.entries(data.breakdown)) {
          let label, imgSrc;
          if (winner === 'character') {
            label = data.character.name;
            imgSrc = data.character.pfp || "/static/icons/default_pfp.png";
          } else if (winner === 'enemy') {
            label = enemy.name;
            imgSrc = enemy.pfp || '/static/images/favicon.png';
          } else {
            label = 'Draw';
            imgSrc = null;
          }
          const card = document.createElement('div');
          card.className = 'col';
          card.innerHTML = `
            <div class="border rounded-3 p-2">
              <h6 class="fw-bold mb-2">${attr}</h6>
              ${imgSrc ? `<img src="${imgSrc}" width="80" height="80" class="rounded-circle mb-1">` : ''}
              <div class="small">${label}</div>
            </div>`;
          grid.appendChild(card);
        }

        lastResult = data.result;
        resultModal.show();
      });
    });

    resultClose.addEventListener('click', function () {
      resultModal.hide();
      if (lastResult === 'game_over' || lastResult === 'win') {
        fetch('/api/reset-character', { method: 'POST' })
          .then(() => { window.location.href = '/gauntlet_waves'; });
      } else {
        location.reload();
      }
    });
  }
});
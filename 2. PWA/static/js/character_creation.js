document.addEventListener("DOMContentLoaded", function () {
  const rollBtn = document.getElementById("roll-btn");
  const finaliseBtn = document.getElementById("finalise-btn");
  const modalElement = document.getElementById("rollResultModal");
  const modalSpecies = document.getElementById("modal-species");
  const modalAttributes = document.getElementById("modal-attributes");
  if (!rollBtn) return;

  let rolledAttributes = {};
  const rollModal = modalElement ? new bootstrap.Modal(modalElement) : null;

  function rarityClass(rarity) {
    return "rarity-" + String(rarity || "").replace(/\s+/g, "");
  }

  function renderAttributeChip(el, rollData) {
    if (!el) return;
    const level = rollData && rollData.level ? rollData.level : "-";
    const rarity = rollData && rollData.rarity ? rollData.rarity : "-";
    const rarityCss = rarityClass(rarity);
    el.innerHTML =
      '<span class="roll-level">' +
      level +
      '</span><span class="roll-rarity ' +
      rarityCss +
      '">(' +
      rarity +
      ")</span>";
  }

  function renderRollModal(species, attributes) {
    if (!rollModal || !modalSpecies || !modalAttributes) return;
    modalSpecies.textContent = species || "-";
    modalAttributes.innerHTML = "";
    for (const [attr, rollData] of Object.entries(attributes || {})) {
      const rarityCss = rarityClass(rollData.rarity);
      const li = document.createElement("li");
      li.className = "list-group-item d-flex justify-content-between align-items-center";
      li.innerHTML =
        "<span>" +
        attr +
        "</span>" +
        '<span><strong class="roll-level">' +
        rollData.level +
        '</strong><span class="roll-rarity ' +
        rarityCss +
        '"> (' +
        rollData.rarity +
        ")</span></span>";
      modalAttributes.appendChild(li);
    }
    rollModal.show();
  }

  rollBtn.addEventListener("click", async function () {
    const name = document.getElementById("char-name").value.trim();
    if (!name) {
      alert("Please enter a character name before rolling.");
      return;
    }

    rollBtn.disabled = true;
    rollBtn.textContent = "Rolling…";

    try {
      const response = await fetch("/api/roll-preview");
      if (!response.ok) {
        alert("Failed to roll. Please try again.");
        return;
      }
      const data = await response.json();

      document.getElementById("char-species").value = data.species;
      document.getElementById("species-id").value = data.species_id;

      for (const [attr, rollData] of Object.entries(data.attributes)) {
        const el = document.getElementById("attr-" + attr);
        renderAttributeChip(el, rollData);
      }
      rolledAttributes = data.attributes;
      finaliseBtn.disabled = false;
      renderRollModal(data.species, data.attributes);
    } catch {
      alert("Error connecting to server. Please try again.");
    } finally {
      rollBtn.disabled = false;
      rollBtn.textContent = "Re-roll Species & Attributes";
    }
  });

  finaliseBtn.addEventListener("click", async function () {
    const name = document.getElementById("char-name").value.trim();
    const speciesId = parseInt(document.getElementById("species-id").value, 10);
    const csrfToken = document.getElementById("csrf-token").value;

    if (!name || !speciesId) {
      alert("Please roll before finalising.");
      return;
    }

    finaliseBtn.disabled = true;
    finaliseBtn.textContent = "Saving…";

    try {
      const response = await fetch("/api/create-character", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
          name: name,
          species_id: speciesId,
          attributes: rolledAttributes,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        alert(data.error || "Failed to save character.");
        finaliseBtn.disabled = false;
        finaliseBtn.textContent = "Finalise Character";
        return;
      }

      window.location.href = "/character-creation";
    } catch {
      alert("Error saving character. Please try again.");
      finaliseBtn.disabled = false;
      finaliseBtn.textContent = "Finalise Character";
    }
  });
});

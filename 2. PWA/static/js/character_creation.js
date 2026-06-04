document.addEventListener("DOMContentLoaded", function () {
  const rollBtn = document.getElementById("roll-btn");
  const finaliseBtn = document.getElementById("finalise-btn");
  const modalElement = document.getElementById("rollResultModal");
  const modalSpecies = document.getElementById("modal-species");
  const modalAttributes = document.getElementById("modal-attributes");
  const pfpInput = document.getElementById("char-pfp");
  const pfpPreview = document.getElementById("char-pfp-preview");
  const pfpPlaceholder = document.getElementById("char-pfp-placeholder");
  const pfpHiddenData = document.getElementById("char-pfp-data");
  const pfpModalElement = document.getElementById("pfpCropModal");
  const pfpCropStage = document.getElementById("pfp-crop-stage");
  const pfpCropImage = document.getElementById("pfp-crop-image");
  const pfpCropConfirm = document.getElementById("pfp-crop-confirm");
  const pfpZoom = document.getElementById("pfp-zoom");
  if (!rollBtn) return;

  const ATTRIBUTE_ORDER = ["BIQ", "IQ", "Speed", "Stamina", "Durability", "Strength"];
  let finalPfpDataUrl = "";
  const rollModal = modalElement ? new bootstrap.Modal(modalElement) : null;
  const pfpModal = pfpModalElement ? new bootstrap.Modal(pfpModalElement) : null;

  const cropState = {
    img: null,
    x: 0,
    y: 0,
    scale: 1,
    minScale: 1,
    dragging: false,
    dragOffsetX: 0,
    dragOffsetY: 0,
  };

  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function getCircleBounds() {
    if (!pfpCropStage) return { x: 0, y: 0, size: 0 };
    const stageSize = pfpCropStage.clientWidth;
    const size = stageSize * 0.72;
    const offset = stageSize * 0.14;
    return { x: offset, y: offset, size: size };
  }

  function constrainCropPosition() {
    if (!cropState.img || !pfpCropStage) return;
    const circle = getCircleBounds();
    const scaledW = cropState.img.width * cropState.scale;
    const scaledH = cropState.img.height * cropState.scale;

    const minX = circle.x + circle.size - scaledW;
    const maxX = circle.x;
    const minY = circle.y + circle.size - scaledH;
    const maxY = circle.y;

    cropState.x = clamp(cropState.x, minX, maxX);
    cropState.y = clamp(cropState.y, minY, maxY);
  }

  function renderCropImage() {
    if (!cropState.img || !pfpCropImage) return;
    pfpCropImage.style.width = cropState.img.width + "px";
    pfpCropImage.style.height = cropState.img.height + "px";
    pfpCropImage.style.transform =
      "translate(" + cropState.x + "px, " + cropState.y + "px) scale(" + cropState.scale + ")";
  }

  function openCropModalFromFile(file) {
    if (!file || !file.type || !file.type.startsWith("image/")) {
      alert("Please choose an image file.");
      return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
      const img = new Image();
      img.onload = function () {
        if (!pfpCropStage || !pfpCropImage) return;

        cropState.img = img;
        const stageSize = pfpCropStage.clientWidth || 320;
        const circle = getCircleBounds();
        const requiredScale = Math.max(circle.size / img.width, circle.size / img.height);

        cropState.minScale = requiredScale;
        cropState.scale = requiredScale;
        if (pfpZoom) {
          pfpZoom.min = String(requiredScale);
          pfpZoom.value = String(requiredScale);
        }

        cropState.x = (stageSize - img.width * cropState.scale) / 2;
        cropState.y = (stageSize - img.height * cropState.scale) / 2;
        constrainCropPosition();
        pfpCropImage.src = e.target.result;
        renderCropImage();
        if (pfpModal) pfpModal.show();
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }

  function onPasteImage(event) {
    const items = event.clipboardData && event.clipboardData.items;
    if (!items) return;

    for (const item of items) {
      if (item.type && item.type.startsWith("image/")) {
        const file = item.getAsFile();
        if (file) {
          event.preventDefault();
          openCropModalFromFile(file);
          return;
        }
      }
    }
  }

  function setPreviewImage(dataUrl) {
    finalPfpDataUrl = dataUrl;
    if (pfpPreview) {
      pfpPreview.src = dataUrl;
      pfpPreview.style.display = "block";
    }
    if (pfpPlaceholder) pfpPlaceholder.style.display = "none";
    if (pfpHiddenData) pfpHiddenData.value = dataUrl;
  }

  if (pfpInput) {
    pfpInput.addEventListener("change", function () {
      const file = pfpInput.files && pfpInput.files[0];
      if (file) openCropModalFromFile(file);
    });
  }

  document.addEventListener("paste", onPasteImage);

  if (pfpCropStage) {
    pfpCropStage.addEventListener("mousedown", function (event) {
      if (!cropState.img) return;
      cropState.dragging = true;
      cropState.dragOffsetX = event.clientX - cropState.x;
      cropState.dragOffsetY = event.clientY - cropState.y;
      pfpCropStage.classList.add("dragging");
    });

    window.addEventListener("mousemove", function (event) {
      if (!cropState.dragging) return;
      cropState.x = event.clientX - cropState.dragOffsetX;
      cropState.y = event.clientY - cropState.dragOffsetY;
      constrainCropPosition();
      renderCropImage();
    });

    window.addEventListener("mouseup", function () {
      cropState.dragging = false;
      pfpCropStage.classList.remove("dragging");
    });
  }

  if (pfpZoom) {
    pfpZoom.addEventListener("input", function () {
      if (!cropState.img) return;
      const nextScale = Math.max(parseFloat(pfpZoom.value), cropState.minScale);
      const stageCenter = pfpCropStage.clientWidth / 2;
      const imagePointX = (stageCenter - cropState.x) / cropState.scale;
      const imagePointY = (stageCenter - cropState.y) / cropState.scale;

      cropState.scale = nextScale;
      cropState.x = stageCenter - imagePointX * cropState.scale;
      cropState.y = stageCenter - imagePointY * cropState.scale;
      constrainCropPosition();
      renderCropImage();
    });
  }

  if (pfpCropConfirm) {
    pfpCropConfirm.addEventListener("click", function () {
      if (!cropState.img || !pfpCropStage) return;

      const circle = getCircleBounds();
      const sourceX = (circle.x - cropState.x) / cropState.scale;
      const sourceY = (circle.y - cropState.y) / cropState.scale;
      const sourceSize = circle.size / cropState.scale;

      const canvas = document.createElement("canvas");
      const size = 256;
      canvas.width = size;
      canvas.height = size;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      ctx.beginPath();
      ctx.arc(size / 2, size / 2, size / 2, 0, Math.PI * 2);
      ctx.closePath();
      ctx.clip();
      ctx.drawImage(cropState.img, sourceX, sourceY, sourceSize, sourceSize, 0, 0, size, size);

      const dataUrl = canvas.toDataURL("image/png");
      setPreviewImage(dataUrl);
      if (pfpModal) pfpModal.hide();
    });
  }

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
    for (const attr of ATTRIBUTE_ORDER.slice().reverse()) {
      const rollData = attributes && attributes[attr];
      if (!rollData) continue;
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

      for (const attr of ATTRIBUTE_ORDER.slice().reverse()) {
        const rollData = data.attributes && data.attributes[attr];
        if (!rollData) continue;
        const el = document.getElementById("attr-" + attr);
        renderAttributeChip(el, rollData);
      }
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
    const csrfToken = document.getElementById("csrf-token").value;

    if (!name) {
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
        body: JSON.stringify({ name: name }),
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

  function enterEditMode(wrap) {
    const display = wrap.querySelector(".character-name-display");
    const input = wrap.querySelector(".character-name-input");
    if (!display || !input) return;
    input.value = display.textContent.trim();
    display.classList.add("d-none");
    input.classList.remove("d-none");
    input.focus();
    input.select();
  }

  function exitEditMode(wrap) {
    const display = wrap.querySelector(".character-name-display");
    const input = wrap.querySelector(".character-name-input");
    if (!display || !input) return;
    input.classList.add("d-none");
    display.classList.remove("d-none");
  }

  async function saveCharacterName(wrap) {
    const display = wrap.querySelector(".character-name-display");
    const input = wrap.querySelector(".character-name-input");
    const characterId = wrap.dataset.characterId;
    const csrfToken = document.getElementById("csrf-token").value;
    const newName = input.value.trim();
    const currentName = display.textContent.trim();

    if (!newName || newName === currentName) {
      input.value = currentName;
      exitEditMode(wrap);
      return;
    }

    try {
      const response = await fetch("/api/rename-character", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ character_id: Number(characterId), name: newName }),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        alert(data.error || "Failed to rename character.");
        input.value = currentName;
        exitEditMode(wrap);
        return;
      }

      const data = await response.json();
      display.textContent = data.name;
      exitEditMode(wrap);
    } catch {
      alert("Error connecting to server. Please try again.");
      input.value = currentName;
      exitEditMode(wrap);
    }
  }

  document.querySelectorAll(".character-name-wrap").forEach(function (wrap) {
    const editBtn = wrap.querySelector(".character-name-edit");
    const input = wrap.querySelector(".character-name-input");

    if (editBtn) {
      editBtn.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();
        enterEditMode(wrap);
      });
    }

    if (input) {
      input.addEventListener("click", function (event) {
        event.stopPropagation();
      });
      input.addEventListener("keydown", function (event) {
        event.stopPropagation();
        if (event.key === "Enter") {
          event.preventDefault();
          saveCharacterName(wrap);
        } else if (event.key === "Escape") {
          event.preventDefault();
          exitEditMode(wrap);
        }
      });
      input.addEventListener("blur", function () {
        if (!input.classList.contains("d-none")) {
          saveCharacterName(wrap);
        }
      });
    }
  });
});

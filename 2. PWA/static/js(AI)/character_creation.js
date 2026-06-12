document.addEventListener("DOMContentLoaded", function () {
  const pfpInput = document.getElementById("char-pfp");
  const pfpPreview = document.getElementById("char-pfp-preview");
  const pfpPlaceholder = document.getElementById("char-pfp-placeholder");
  const pfpHiddenData = document.getElementById("char-pfp-data");
  const pfpModalElement = document.getElementById("pfpCropModal");
  const pfpCropStage = document.getElementById("pfp-crop-stage");
  const pfpCropImage = document.getElementById("pfp-crop-image");
  const pfpCropConfirm = document.getElementById("pfp-crop-confirm");
  const pfpZoom = document.getElementById("pfp-zoom");
  if (!pfpInput && !pfpCropStage) return;

  let editingCharacterId = null;
  let editingPfpImgEl = null;
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
    const stageSize = pfpCropStage.clientWidth || 320;
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

    const MAX_SIZE_MB = 60;
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
      alert("Image must be under " + MAX_SIZE_MB + "MB.");
      return;
    }

    // Read first 6 bytes to detect GIF magic bytes (GIF87a / GIF89a)
    const headerSlice = file.slice(0, 6);
    const headerReader = new FileReader();
    headerReader.onload = function (headerEvt) {
      const bytes = new Uint8Array(headerEvt.target.result);
      // GIF magic: 47 49 46 38 (G I F 8)
      const isGifBytes = bytes[0] === 0x47 && bytes[1] === 0x49 && bytes[2] === 0x46 && bytes[3] === 0x38;
      const isGif = isGifBytes || file.type === "image/gif" || file.name.toLowerCase().endsWith(".gif");
      if (isGif) {
        const gifReader = new FileReader();
        gifReader.onload = function (e) {
          if (editingCharacterId) {
            const csrfToken = document.getElementById("csrf-token").value;
            fetch("/api/edit-pfp", {
              method: "POST",
              headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
              body: JSON.stringify({ character_id: Number(editingCharacterId), profile_image: e.target.result }),
            }).then(function (response) {
              if (!response.ok) {
                return response.json().then(function (d) { alert(d.error || "Failed to update photo."); });
              }
              if (editingPfpImgEl) {
                editingPfpImgEl.src = e.target.result;
                editingPfpImgEl.classList.remove("d-none");
                editingPfpImgEl.classList.add("pfp-has-image");
                const wrap = editingPfpImgEl.closest(".pfp-preview-wrap");
                if (wrap) {
                  const placeholder = wrap.querySelector(".pfp-preview-placeholder");
                  if (placeholder) placeholder.classList.add("d-none");
                }
              }
              editingCharacterId = null;
              editingPfpImgEl = null;
            }).catch(function () {
              alert("Error connecting to server (GIF edit).");
              editingCharacterId = null;
              editingPfpImgEl = null;
            });
          } else {
            setPreviewImage(e.target.result);
          }
        };
        gifReader.readAsDataURL(file);
      } else {
        // Not a GIF — open crop modal
        const reader = new FileReader();
        reader.onload = function (e) {
          const img = new Image();
          img.onload = function () {
            if (!pfpCropStage || !pfpCropImage) return;

            cropState.img = img;
            pfpCropImage.src = e.target.result;
            if (pfpModal) pfpModal.show();

            // Wait for modal to be visible so clientWidth is correct
            setTimeout(function () {
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
              renderCropImage();
            }, 150);
          };
          img.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    };
    headerReader.readAsArrayBuffer(headerSlice);
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
    if (pfpPreview) {
      pfpPreview.src = dataUrl;
      pfpPreview.classList.add("pfp-has-image");
    }
    if (pfpPlaceholder) pfpPlaceholder.classList.add("d-none");
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

    pfpCropStage.addEventListener("wheel", function (event) {
      if (!cropState.img) return;
      event.preventDefault();
      const delta = event.deltaY > 0 ? -0.05 : 0.05;
      const nextScale = Math.max(cropState.minScale, cropState.scale + delta);
      const stageCenter = pfpCropStage.clientWidth / 2;
      const imagePointX = (stageCenter - cropState.x) / cropState.scale;
      const imagePointY = (stageCenter - cropState.y) / cropState.scale;

      cropState.scale = nextScale;
      cropState.x = stageCenter - imagePointX * cropState.scale;
      cropState.y = stageCenter - imagePointY * cropState.scale;
      if (pfpZoom) pfpZoom.value = String(nextScale);
      constrainCropPosition();
      renderCropImage();
    }, { passive: false });
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

      if (editingCharacterId) {
        // Editing an existing character's pfp
        const csrfToken = document.getElementById("csrf-token").value;
        fetch("/api/edit-pfp", {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
          body: JSON.stringify({ character_id: Number(editingCharacterId), profile_image: dataUrl }),
        }).then(function (response) {
          if (!response.ok) {
            return response.json().then(function (d) { alert(d.error || "Failed to update photo."); });
          }
          if (editingPfpImgEl) {
            editingPfpImgEl.src = dataUrl;
            editingPfpImgEl.classList.remove("d-none");
            const wrap = editingPfpImgEl.closest(".pfp-preview-wrap");
            if (wrap) {
              const placeholder = wrap.querySelector(".pfp-preview-placeholder");
              if (placeholder) placeholder.classList.add("d-none");
            }
          }
          editingCharacterId = null;
          editingPfpImgEl = null;
          if (pfpModal) pfpModal.hide();
        }).catch(function () {
          alert("Error connecting to server (crop save).");
          editingCharacterId = null;
          editingPfpImgEl = null;
        });
      } else {
        // New character creation
        setPreviewImage(dataUrl);
        if (pfpModal) pfpModal.hide();
      }
    });
  }


  // Reset editing state if crop modal is dismissed without confirming
  if (pfpModalElement) {
    pfpModalElement.addEventListener("hidden.bs.modal", function () {
      editingCharacterId = null;
      editingPfpImgEl = null;
    });
  }

  // Handle "Change Photo" file input in the character list
  document.addEventListener("change", function (event) {
    if (!event.target.classList.contains("pfp-edit-input")) return;
    const file = event.target.files && event.target.files[0];
    const label = event.target.closest("[data-character-id]");
    if (!file || !label) return;
    editingCharacterId = label.dataset.characterId;
    editingPfpImgEl = label.closest("details").querySelector(".pfp-preview");
    openCropModalFromFile(file);
    event.target.value = "";
  });

});

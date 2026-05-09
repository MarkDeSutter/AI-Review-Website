/* ToolRank — main.js */

// ── Interactive star picker in review form ──
(function () {
  const picker = document.getElementById("star-picker");
  if (!picker) return;

  const stars  = picker.querySelectorAll(".star-pick");
  const hidden = document.getElementById("rating-input");

  function setRating(val) {
    stars.forEach((s, i) => {
      s.classList.toggle("filled", i < val);
    });
    hidden.value = val;
  }

  // Init from existing value
  setRating(parseInt(hidden.value) || 3);

  stars.forEach((star, idx) => {
    star.addEventListener("mouseenter", () => setRating(idx + 1));
    star.addEventListener("click",      () => setRating(idx + 1));
  });

  picker.addEventListener("mouseleave", () => setRating(parseInt(hidden.value)));
})();

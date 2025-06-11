document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  form.addEventListener("submit", function(event) {
    event.preventDefault();
    alert("Дякуємо! Ваше повідомлення надіслано.");
    form.reset();
  });
});

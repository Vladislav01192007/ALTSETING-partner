document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll("section");

  const revealOnScroll = () => {
    const windowHeight = window.innerHeight;
    sections.forEach(section => {
      const top = section.getBoundingClientRect().top;
      if (top < windowHeight - 100) {
        section.classList.add("visible");
      }
    });
  };

  revealOnScroll();
  window.addEventListener("scroll", revealOnScroll);
});



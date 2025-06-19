document.getElementById('register-btn').addEventListener('click', () => {
  document.getElementById('register-modal').style.display = 'block';
});

document.getElementById('close-modal').addEventListener('click', () => {
  document.getElementById('register-modal').style.display = 'none';
});

window.addEventListener('click', (e) => {
  const modal = document.getElementById('register-modal');
  if (e.target === modal) {
    modal.style.display = 'none';
  }
});

document.getElementById('register-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData);

  try {
    const response = await fetch('/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await response.json();
    const messageEl = document.getElementById('form-message');
    if (response.ok) {
      messageEl.style.color = 'green';
      messageEl.textContent = result.message;
      form.reset();
      setTimeout(() => {
        document.getElementById('register-modal').style.display = 'none';
        window.location.href = '/login';
      }, 2000);
    } else {
      messageEl.style.color = 'red';
      messageEl.textContent = result.error;
    }
  } catch (error) {
    console.error('Error:', error);
    document.getElementById('form-message').textContent = 'Помилка сервера.';
  }
});

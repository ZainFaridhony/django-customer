const showPasswordToggle = document.querySelector('.showPasswordToggle');

showPasswordToggle.addEventListener('click', function (e) {
    // toggle the type attribute
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
  });
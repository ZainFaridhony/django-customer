
const passwordField = document.querySelector('#passwordField');
const confirmPasswordField = document.querySelector('#confirmPasswordField');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const showPasswordToggle2 = document.querySelector('.showPasswordToggle2');

const passwordStrength = document.querySelector('#passwordStrength');

showPasswordToggle.addEventListener('click', function (e) {
  // toggle the type attribute
  const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
  passwordField.setAttribute('type', type);
  // toggle the eye slash icon
  this.classList.toggle('fa-eye-slash');
});

showPasswordToggle2.addEventListener('click', function (e) {
  // toggle the type attribute
  const type = confirmPasswordField.getAttribute('type') === 'password' ? 'text' : 'password';
  confirmPasswordField.setAttribute('type', type);
  // toggle the eye slash icon
  this.classList.toggle('fa-eye-slash');
});

function validatePassword(){
  if(passwordField.value != confirmPasswordField.value) {
    confirmPasswordField.setCustomValidity("Passwords Don't Match");
  } else {
    confirmPasswordField.setCustomValidity('');
  }
};

passwordField.onchange = validatePassword;
confirmPasswordField.onkeyup = validatePassword;

function checkPassword(password) {
  var strength = 0;
  if (password.match(/[a-zA-Z0-9][a-zA-Z0-9]+/)) {
    strength += 1;
  };
  if (password.match(/[~<>?]+/)) {
    strength += 1;
  };
  if (password.match(/[!@#$%^&*()]+/)) {
    strength += 1;
  };
  if (password.length > 5) {
    strength += 1;
  };

  switch (strength) {
    case 0:
      passwordStrength.value = 0;
      break;
    case 1:
      passwordStrength.value = 25;
      break;
    case 2:
      passwordStrength.value = 50;
      break;
    case 3:
      passwordStrength.value = 75;
      break;
    case 4:
      passwordStrength.value = 100;
      break;
  }
};

passwordField.addEventListener('keyup', function() {
  if (passwordField.value.length > 0) {
    checkPassword(passwordField.value);
    passwordStrength.style.display = "block";
  } else {
    passwordStrength.style.display = "none";
  }
  
});

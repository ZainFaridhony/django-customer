const showPasswordToggle=document.querySelector('.showPasswordToggle');showPasswordToggle.addEventListener('click',function(e){const type=passwordField.getAttribute('type')==='password'?'text':'password';passwordField.setAttribute('type',type);this.classList.toggle('fa-eye-slash');});;
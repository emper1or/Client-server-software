// register.js
document.addEventListener('DOMContentLoaded', function () {
    const togglePassword1 = document.querySelector('#togglePassword1');
    const password1 = document.querySelector('#password1');
    const togglePassword2 = document.querySelector('#togglePassword2');
    const password2 = document.querySelector('#password2');

    if (togglePassword1 && password1) {
        togglePassword1.addEventListener('click', function () {
            const type = password1.getAttribute('type') === 'password' ? 'text' : 'password';
            password1.setAttribute('type', type);
            this.classList.toggle('fa-eye-slash');
        });
    }

    if (togglePassword2 && password2) {
        togglePassword2.addEventListener('click', function () {
            const type = password2.getAttribute('type') === 'password' ? 'text' : 'password';
            password2.setAttribute('type', type);
            this.classList.toggle('fa-eye-slash');
        });
    }
});
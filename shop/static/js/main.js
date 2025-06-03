document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('post');
    const usernameInput = document.getElementById('id_username');
    const emailInput = document.getElementById('id_email');
    const passwordInput = document.getElementById('id_password1');
    const errorUsername = document.getElementById('error-username');
    const errorEmail = document.getElementById('error-email');
    const errorPassword = document.getElementById('error-password1');

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])/;
    const digitsPattern = /\d/;

    function validateUsername() {
        const value = usernameInput.value.trim();
        const firstChar = value.charAt(0);

        if (digitsPattern.test(value)) {
            showError(usernameInput, errorUsername, 'Имя должно состоять только из букв');
            return false;
        }
        if (value === "") {
            showError(usernameInput, errorUsername, 'Имя не должно быть пустым');
            return false;
        }
        if (firstChar !== firstChar.toUpperCase()) {
            showError(usernameInput, errorUsername, 'Имя должно начинаться с заглавной буквы');
            return false;
        }

        hideError(usernameInput, errorUsername);
        return true;
    }

    function validateEmail() {
        const value = emailInput.value.trim();

        if (value === "") {
            showError(emailInput, errorEmail, 'Email не должен быть пустым');
            return false;
        }
        if (!emailPattern.test(value)) {
            showError(emailInput, errorEmail, 'Пожалуйста, введите правильный email');
            return false;
        }

        hideError(emailInput, errorEmail);
        return true;
    }

    function validatePassword() {
        const value = passwordInput.value;

        if (value === "") {
            showError(passwordInput, errorPassword, 'Пароль не должен быть пустым');
            return false;
        }
        if (value.length < 8) {
            showError(passwordInput, errorPassword, 'Пароль должен быть не менее 8 символов');
            return false;
        }
        if (!passwordPattern.test(value)) {
            showError(passwordInput, errorPassword, 'Пароль должен содержать буквы, цифры и спецсимволы (!@#$%^&*)');
            return false;
        }

        hideError(passwordInput, errorPassword);
        return true;
    }

    function showError(input, errorElement, message) {
        input.classList.add('invalid');
        errorElement.textContent = message;
    }

    function hideError(input, errorElement) {
        input.classList.remove('invalid');
        errorElement.textContent = '';
    }

    usernameInput.addEventListener('blur', validateUsername);
    emailInput.addEventListener('blur', validateEmail);
    passwordInput.addEventListener('blur', validatePassword);

    usernameInput.addEventListener('focus', () => {
        if (usernameInput.classList.contains('invalid')) hideError(usernameInput, errorUsername);
    });

    emailInput.addEventListener('focus', () => {
        if (emailInput.classList.contains('invalid')) hideError(emailInput, errorEmail);
    });

    passwordInput.addEventListener('focus', () => {
        if (passwordInput.classList.contains('invalid')) hideError(passwordInput, errorPassword);
    });

    form.addEventListener('submit', function (event) {
        const isUsernameValid = validateUsername();
        const isEmailValid = validateEmail();
        const isPasswordValid = validatePassword();

        if (!isUsernameValid || !isEmailValid || !isPasswordValid) {
            event.preventDefault();
            if (!isUsernameValid) usernameInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            else if (!isEmailValid) emailInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            else passwordInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    });
});

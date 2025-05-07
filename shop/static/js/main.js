document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('post');
    const usernameInput = document.getElementById('id_username');
    const emailInput = document.getElementById('id_email');
    const passwordInput = document.getElementById('id_password1');
    const errorUsername = document.getElementById('error-username');
    const errorEmail = document.getElementById('error-email');
    const errorPassword = document.getElementById('error-password1');

    // Паттерны для валидации
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])/;
    const digitsPattern = /\d/;

    // Валидация имени пользователя
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

    // Валидация email
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

    // Валидация пароля
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
            showError(passwordInput, errorPassword, 'Пароль должен содержать буквы, цифры и специальные символы (!@#$%^&*)');
            return false;
        }

        hideError(passwordInput, errorPassword);
        return true;
    }

    // Вспомогательные функции
    function showError(input, errorElement, message) {
        input.classList.add('invalid');
        errorElement.textContent = message;
    }

    function hideError(input, errorElement) {
        input.classList.remove('invalid');
        errorElement.textContent = '';
    }

    // Обработчики событий
    usernameInput.addEventListener('blur', validateUsername);
    emailInput.addEventListener('blur', validateEmail);
    passwordInput.addEventListener('blur', validatePassword);

    usernameInput.addEventListener('focus', function() {
        if (this.classList.contains('invalid')) {
            hideError(this, errorUsername);
        }
    });

    emailInput.addEventListener('focus', function() {
        if (this.classList.contains('invalid')) {
            hideError(this, errorEmail);
        }
    });

    passwordInput.addEventListener('focus', function() {
        if (this.classList.contains('invalid')) {
            hideError(this, errorPassword);
        }
    });

    // Валидация при отправке формы
    form.addEventListener('submit', function(event) {
        const isUsernameValid = validateUsername();
        const isEmailValid = validateEmail();
        const isPasswordValid = validatePassword();

        if (!isUsernameValid || !isEmailValid || !isPasswordValid) {
            event.preventDefault();

            // Прокрутка к первой ошибке
            if (!isUsernameValid) {
                usernameInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else if (!isEmailValid) {
                emailInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
                passwordInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });
});

const url = likeUrl;
var csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
var options = {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin'
}

document.getElementById('like-btn').addEventListener('click', async function(e) {
    e.preventDefault();
    const likeButton = this;

    try {
        const response = await fetch(likeUrl, {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
        'id': likeButton.dataset.id,
        'action': likeButton.dataset.action,
    }),
});

        const data = await response.json();

        if (data.status === 'ok') {
            // Обновляем текст кнопки
            const newAction = likeButton.dataset.action === 'like' ? 'unlike' : 'like';
            likeButton.dataset.action = newAction;
            likeButton.textContent = newAction === 'like' ? 'Like' : 'Unlike';

            // Обновляем количество лайков
            document.querySelectorAll('.total-likes, .total').forEach(el => {
                el.textContent = data.likes_count;
            });
        } else {
            console.error('Error:', data.message || 'Unknown error');
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
});
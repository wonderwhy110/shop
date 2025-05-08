FROM python:3.12.0

SHELL ["/bin/bash", "-c"]

# Устанавливаем переменные среды
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Обновление pip
RUN pip install --upgrade pip

# Обновление репозиториев и установка необходимых библиотек
RUN apt update && apt -qy install \
    gcc \
    libjpeg-dev \
    libxslt-dev \
    libpq-dev \
    libmariadb-dev \
    libmariadb-dev-compat \
    gettext \
    cron \
    openssh-client \
    flake8

# Создаем пользователя и устанавливаем права
RUN useradd -rms /bin/bash sh && chmod 777 /opt /run

# Устанавливаем рабочую директорию
WORKDIR /sh

# Создаем необходимые директории
RUN mkdir /sh/static && mkdir /sh/media && chown -R sh:sh /sh && chmod 755 /sh

# Копируем проект в контейнер
COPY --chown=sh:sh . .

# Устанавливаем зависимости из requirements.txt
RUN pip install -r requirements.txt

# Переключаемся на пользователя sh
USER sh

# Запускаем приложение Django через manage.py
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

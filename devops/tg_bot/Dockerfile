FROM python:3.10.11 as base-image

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /code

# Устанавливаем зависимости для компиляции
RUN apt-get update \
 && apt-get install -y gcc

# Копируем файлы зависимостей и устанавливаем их
COPY ../../requirements.txt requirements.txt
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

# Устанавливаем neovim
RUN apt-get install -y curl
RUN curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage \
    && chmod u+x nvim.appimage \
    && ./nvim.appimage --appimage-extract \
    && mv squashfs-root /opt/nvim \
    && ln -s /opt/nvim/usr/bin/nvim /usr/local/bin/nvim

# Копируем и настраиваем приложение
COPY ../../src/telegram_bot /code/src

# Устанавливаем права доступа
USER root
RUN chown -R nobody:nogroup /code
RUN chmod -R 777 /code

# Переключаемся на непривилегированного пользователя
USER nobody:nogroup

# Проверяем доступность сервиса
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:5000/ || exit 1

#ENTRYPOINT aerich init -t src.model.database.config.DATABASE_CONFIG && \
#           aerich init-db && \
#           aerich migrate && \
#           python3 -u src/__main__.py

ENTRYPOINT cd src/ && alembic revision --autogenerate && \
           alembic  upgrade head && \
           python3 -u __main__.py
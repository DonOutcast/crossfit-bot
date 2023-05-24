FROM python:3.10.11 as base-image

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

WORKDIR /code
ADD ../../requirements.txt requirements.txt
RUN python -m venv /opt/venv

RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"

ENV PATH="/opt/venv/bin:$PATH"
RUN apt-get update \
 && apt-get install -y gcc \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt \
 && rm -rf /var/lib/apt/lists/* \

RUN curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage \
    && chmod u+x nvim.appimage \
    && ./nvim.appimage --appimage-extract \
    && mv squashfs-root /opt/nvim \
    && ln -s /opt/nvim/usr/bin/nvim /usr/local/bin/nvim \

COPY ../../src/telegram_bot src
USER nobody:nogroup
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:5000/ || exit 1

CMD ["python3", "-u", "src/__main__.py"]

FROM elasticsearch:7.17.9
USER root
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get install -y git

RUN curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage \
    && chmod u+x nvim.appimage \
    && ./nvim.appimage --appimage-extract \
    && mv squashfs-root /opt/nvim \
    && ln -s /opt/nvim/usr/bin/nvim /usr/local/bin/nvim

COPY elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml

USER elasticsearch

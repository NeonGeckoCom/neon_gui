FROM python:3.10-slim

LABEL vendor=neon.ai \
    ai.neon.name="neon-gui"

ENV OVOS_CONFIG_BASE_FOLDER neon
ENV OVOS_CONFIG_FILENAME neon.yaml
ENV XDG_CONFIG_HOME /config

EXPOSE 18181

RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    swig \
    libssl-dev \
    libfann-dev

ADD . /neon_gui
WORKDIR /neon_gui

RUN pip install wheel \
    && pip install .[docker]

COPY docker_overlay/ /

CMD ["neon-gui", "run"]
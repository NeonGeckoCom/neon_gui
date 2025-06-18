FROM python:3.10-slim

LABEL vendor=neon.ai \
    ai.neon.name="neon-gui"

ENV OVOS_CONFIG_BASE_FOLDER=neon
ENV OVOS_CONFIG_FILENAME=neon.yaml
ENV XDG_CONFIG_HOME=/config

EXPOSE 18181

RUN apt-get update && \
    apt-get install -y \
    git \
    gcc \
    g++ \
    python3-dev \
    swig \
    libssl-dev \
    libfann-dev

COPY . /neon_gui
WORKDIR /neon_gui

RUN pip install --no-cache-dir wheel \
    && pip install --no-cache-dir .[docker]

COPY docker_overlay/ /
HEALTHCHECK CMD "/opt/neon/healthcheck.sh"
CMD ["neon-gui", "run", "-p", "8000"]

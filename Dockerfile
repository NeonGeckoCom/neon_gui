FROM python:3.8-slim

LABEL vendor=neon.ai \
    ai.neon.name="neon-gui"

ENV NEON_CONFIG_PATH /config

RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    swig \
    libssl-dev \
    libfann-dev

RUN apt-get install -y git
# TODO: Remove after neon-utils release

ADD . /neon_gui
WORKDIR /neon_gui

RUN pip install wheel \
    && pip install .[docker]

COPY docker_overlay/ /

CMD ["neon_gui_service"]
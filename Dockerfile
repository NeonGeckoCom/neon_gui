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

ADD . /neon_gui
WORKDIR /neon_gui

RUN pip install wheel \
    && pip install .[docker]

CMD ["neon_gui_service"]
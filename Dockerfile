FROM python:3.8

ADD . /neon_core
WORKDIR /neon_core

RUN apt-get update && \
    apt-get install -y \
    gcc \
    python3-dev \
    swig \
    libssl-dev  \
    libfann-dev \
    && pip install wheel \
    && pip install .

CMD ["neon_gui_service"]
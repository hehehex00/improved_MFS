FROM registry.wildfireworkspace.com/eop/streamlit-1.0/debian:trixie
WORKDIR /datatoolbox

RUN apt-get update && apt-get install -y ca-certificates

RUN apt-get install -y \
    python3.12 \
    python3.12-dev \
    python3-pip \
    build-essential \
    libgdal-dev \
    && apt-get clean

RUN apt install -y python3.12-venv
ENV PATH="/opt/venv/bin:$PATH"
RUN python3.12 -m venv /opt/venv

RUN pip install --upgrade pip wheel setuptools

RUN sed -i 's|http:|https:|' /etc/apt/sources.list.d/debian.sources

RUN apt clean

COPY DEFAULT_BASE_IMAGE/default_requirements.txt /datatoolbox/default_requirements.txt
RUN pip install -r ./default_requirements.txt --timeout=12000

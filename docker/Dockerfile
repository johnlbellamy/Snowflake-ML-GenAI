FROM ubuntu:22.04
LABEL authors="johnbellamy"
ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /app
COPY app/app.py /app/app.py
COPY app/model.py /app/model.py
COPY app/model_input.py /app/model_input.py
COPY requirements /app/requirements

RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y python3.10 python3-dev python3-venv gcc
WORKDIR /app
RUN python3 -m venv .venv && \
    .venv/bin/pip install --no-cache-dir -r requirements


CMD [".venv/bin/fastapi", "run", "app.py", "--port", "5000"]

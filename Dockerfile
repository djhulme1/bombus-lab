# The Bombus lab's experiment environment: what every bundle in this repository runs in.
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 PIP_NO_CACHE_DIR=1
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-deps --only-binary=:all: -r /tmp/requirements.txt && rm /tmp/requirements.txt
RUN useradd --create-home --uid 10001 lab
USER lab
WORKDIR /work

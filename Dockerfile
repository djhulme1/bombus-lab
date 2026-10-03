# The Bombus lab's experiment environment: what every bundle in this repository runs in.
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 PIP_NO_CACHE_DIR=1
COPY requirements.txt /tmp/requirements.txt
# torch comes from PyTorch's CPU-only index (requirements.txt pins torch==<version>+cpu): no CUDA libraries in the image.
RUN pip install --no-deps --only-binary=:all: --extra-index-url https://download.pytorch.org/whl/cpu -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt
RUN useradd --create-home --uid 10001 lab
USER lab
WORKDIR /work

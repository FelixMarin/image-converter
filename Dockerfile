FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependencias del sistema necesarias para Cairo, Pillow y compilación
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
        libcairo2 \
        libcairo2-dev \
        libpango-1.0-0 \
        libpango1.0-dev \
        libgdk-pixbuf-xlib-2.0-0 \
        libgdk-pixbuf-xlib-2.0-dev \
        pkg-config \
        rustc \
        cargo \
        inkscape \
        poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar e instalar dependencias Python primero para aprovechar cache de Docker
COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . /app

# Entrypoint por defecto — ajustar si necesita argumentos o servicio diferente
CMD ["python", "main.py"]

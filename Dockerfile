FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libegl1 \
    libfontconfig1 \
    libglib2.0-0 \
    dbus \
    libxcb-cursor0 \
    libxkbcommon-x11-0 \
    libxcb-keysyms1 \
    libxcb-icccm4 \
    libxcb-shape0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]

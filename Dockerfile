# Dockerfile
FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# 1. Cài các gói hệ thống cần thiết cho GUI ảo & PyAutoGUI
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget gnupg2 ca-certificates \
    xvfb openbox x11-utils x11-xserver-utils xauth \
    xvfb openbox x11-utils scrot libx11-6 libxrender1 libxtst6 libxi6 \
    wget curl fonts-liberation \
    scrot \
    libxtst6 libxrender1 libxi6 libx11-6 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# 2. Cài Chrome
RUN wget -qO- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
      > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y --no-install-recommends google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# 3. Copy code & cài Python packages
WORKDIR /app
COPY . /app

# Yêu cầu Python packages
RUN pip install --no-cache-dir \
    pyautogui pygetwindow pillow opencv-python requests PyYAML

# 4. Chạy Xvfb + openbox + main.py
ENV DISPLAY=:99
CMD sh -c "Xvfb :99 -screen 0 1280x720x24 & \
           sleep 10 && openbox & \
           python /app/main.py"

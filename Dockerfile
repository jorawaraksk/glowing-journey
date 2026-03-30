FROM python:3.9-slim-bullseye

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget pv jq python3-dev ffmpeg mediainfo neofetch \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies (including Flask for HTTP ping)
RUN pip3 install --no-cache-dir -r requirements.txt flask

# Expose the port (Render usually expects 10000)
EXPOSE 10000

# Start Flask ping server + your bot in parallel using a custom script
CMD ["bash", "start.sh"]

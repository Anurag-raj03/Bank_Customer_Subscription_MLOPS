FROM python:3.11-slim

WORKDIR /app

# Install Git and required packages
RUN apt-get update && apt-get install -y \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install DVC
RUN pip install --upgrade pip && pip install dvc

# Copy all project files (including the shell script)
COPY . /app/

# Set the entrypoint to the script
ENTRYPOINT ["bash", "dvc_update.sh"]

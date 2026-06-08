FROM python:3.12-slim

#! Upgrading the base image for security patches and bug fixes
RUN apt-get update && apt-get install -y \
    git curl tar wget \
    libpango-1.0-0 libpangoft2-1.0-0 libcairo2 libffi-dev shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

#? Download Gitleaks and install it in the container
RUN wget https://github.com/gitleaks/gitleaks/releases/download/v8.21.2/gitleaks_8.21.2_linux_x64.tar.gz \
    && tar -xzf gitleaks_8.21.2_linux_x64.tar.gz \
    && mv gitleaks /usr/local/bin/gitleaks \
    && chmod +x /usr/local/bin/gitleaks \
    && rm gitleaks_8.21.2_linux_x64.tar.gz

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
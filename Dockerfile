# Base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create the sessions directory for persisting the Telegram session file
RUN mkdir -p /app/src/sessions

# Copy project files
COPY src/ ./src
COPY .env .env

# Ensure the session directory is excluded from git and available
VOLUME ["/app/src/sessions"]

# Run the bot
CMD ["python", "src/main.py"]

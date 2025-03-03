FROM python:3.12-bullseye

# Add metadata to the image
LABEL maintainer="your_email@example.com"
LABEL version="1.0"
LABEL description="Docker image for Molybot"

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copy the rest of the application code
COPY . .

# Create a non-root user and switch to it
RUN useradd -m molybotuser
USER molybotuser

# Set the entrypoint command
CMD ["python", "main.py"]
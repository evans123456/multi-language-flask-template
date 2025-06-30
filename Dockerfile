FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Flask
RUN pip install flask

# Expose the Flask app port
EXPOSE 5009

# Set environment variable so Flask knows the app
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5009

# Run the app
CMD ["python3", "server.py"]

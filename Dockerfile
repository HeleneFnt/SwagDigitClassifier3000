# Use Python image
FROM python:3.11

# Determine working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies via requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Expose app port
EXPOSE 5000

# Launch app
CMD ["python", "app.py"]

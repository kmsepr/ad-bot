# Use Python 3.10 base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the entire project (in case other files are needed)
COPY . .

# Expose a port (useful if your app serves a webhook)
EXPOSE 8000

# Run the bot
CMD ["python", "olx.py"]
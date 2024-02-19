# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Default values for environment variables (placeholders)
ENV DAGSHUB_USER=default_user
ENV DAGSHUB_TOKEN=default_token

# Run app.py when the container launches
CMD ["python", "src/train_model.py"]

# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY artifacts /app


RUN pip install flask cloudpickle numpy scikit-learn scipy
# Default values for environment variables (placeholders)
EXPOSE 5000

# Run main.py when the container launches
CMD ["python", "main.py"]

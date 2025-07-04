# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=twitter.settings

# Run gunicorn with 4 workers to handle requests on port 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "twitter.wsgi:application"]

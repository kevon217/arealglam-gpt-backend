# Use an official Python runtime as a base image
FROM python:3.11.2

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY ./requirements.txt /app/requirements.txt
COPY ./.env /app/.env
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the app directory contents into the container at /app
COPY ./app /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run your app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

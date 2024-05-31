FROM python:3.12-slim


# Set the working directory to /app
WORKDIR /app

# Install dependencies including libglib2.0-0 for libgthread-2.0.so.0
RUN sudo apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory to /app/api
WORKDIR /app/api

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run uvicorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

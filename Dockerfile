# FROM python:3.10-slim as python-base

# # Env variables
# ENV ENV=staging \
#     PYTHONFAULTHANDLER=1 \
#     PYTHONUNBUFFERED=1 \
#     PYTHONHASHSEED=random \
#     PIP_NO_CACHE_DIR=off \
#     PIP_DISABLE_PIP_VERSION_CHECK=on \
#     PIP_DEFAULT_TIMEOUT=100 \
#     POETRY_VERSION=1.1.12 \
#     PORT=8000

# FROM python-base as builder-base
# # Install gcc compiler since poetry depends on gcc
# RUN apt-get update && apt-get install --no-install-recommends -y \
#     build-essential


# WORKDIR /app
# COPY . /app/


# # Install deps
# RUN pip install -r /app/requirements.txt

# FROM python-base as runtime
# COPY --from=builder-base /usr/local/bin /usr/local/bin
# COPY --from=builder-base /usr/local/lib/python3.10/ /usr/local/lib/python3.10/
# COPY --from=builder-base /app/ /app/

# WORKDIR /app
# COPY . /app

# # This app run in port 8000
# EXPOSE 8000

# WORKDIR /app/api
# # Entry point to our app
# ENTRYPOINT /usr/local/bin/uvicorn app:app --host 0.0.0.0 --port $PORT

# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install dependencies including libglib2.0-0 for libgthread-2.0.so.0
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Set the working directory to /app
WORKDIR /app

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

# A Dockerfile is a text document that contains all the commands
# a user could call on the command line to assemble an image.

# FROM python:3.11-slim

# # Our Debian with python is now installed.
# # Imagine we have folders /sys, /tmp, /bin etc. there
# # like we would install this system on our laptop.

# RUN mkdir build

# # We create folder named build for our stuff.

# WORKDIR /build

# # Basic WORKDIR is just /
# # Now we just want to our WORKDIR to be /build

# COPY . .

# # FROM [path to files from the folder we run docker run]
# # TO [current WORKDIR]
# # We copy our files (files from .dockerignore are ignored)
# # to the WORKDIR

# RUN pip install --no-cache-dir -r requirements.txt

# # OK, now we pip install our requirements

# EXPOSE 80

# # Instruction informs Docker that the container listens on port 80

# WORKDIR /build/api

# # Now we just want to our WORKDIR to be /build/app for simplicity
# # We could skip this part and then type
# # python -m uvicorn main.app:app ... below

# CMD python -m uvicorn app:app --host 0.0.0.0 --port 80

# # This command runs our uvicorn server
# # See Troubleshoots to understand why we need to type in --host 0.0.0.0 and --port 80
# pull base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory to be /code inside docker container
WORKDIR /code


# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt


# Copy project files from local folder to docker's /code/ dir
COPY . /code/

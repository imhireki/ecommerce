FROM python:3.13.1

# Prevent Python from writing pyc and to buffer output
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set working directory inside the container
WORKDIR /code

# Install my dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code into the container
COPY . /code/

EXPOSE 8000

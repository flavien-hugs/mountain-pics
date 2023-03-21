FROM python:3.10

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# copy the requirements file into the image
COPY run.py /app/run.py
COPY requirements.txt /app/requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Exposition du port
EXPOSE 5000

# copy every content from the local file to the image
COPY . /app
CMD ["python", "run.py"]

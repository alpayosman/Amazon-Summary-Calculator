
FROM python:3.9-slim


WORKDIR /app


RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir -r /app/requirements.txt


COPY . /app


EXPOSE 5000


ENV FLASK_APP=app.py


CMD ["flask", "run", "--host=0.0.0.0"]

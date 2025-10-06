FROM python:3.12-slim
RUN useradd -m flaskapp
USER flaskapp

WORKDIR /app

COPY ./app.py ./
COPY ./templates ./templates
COPY ./public_key.pem ./
COPY ./requirements.txt ./

RUN --mount=type=cache,target=/home/flaskapp/.cache/pip \
    pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python3", "app.py"]




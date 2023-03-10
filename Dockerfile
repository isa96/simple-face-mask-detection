FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

COPY requirement.txt .
RUN pip install -r requirement.txt

COPY . .

EXPOSE 8080

CMD [ "python3", "app.py" ]

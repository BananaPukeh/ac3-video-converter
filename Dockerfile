FROM python:3.8

RUN apt update
RUN apt install ffmpeg -y


WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY converter.py .

ENV libraries=""
ENV interval=3600
ENV telegram_token=""
ENV telegram_chat_id=""
ENV replace_original="true"


ENTRYPOINT [ "python", "-u", "converter.py" ]

LABEL MAINTAINER="Rutger Nijhuis"
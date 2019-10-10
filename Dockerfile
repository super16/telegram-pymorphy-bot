FROM python:3.6-alpine3.9
WORKDIR /bot_app
COPY . /bot_app
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev
RUN pip install -r requirements.txt
EXPOSE 80
ENV NAME App
CMD ["python", "bot.py"]

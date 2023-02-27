FROM python:3.11-slim

WORKDIR /bot-app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN ["pip", "install", "poetry"]

COPY . /bot-app

RUN ["poetry", "install", "--without", "development"]

EXPOSE 80

CMD ["poetry", "run", "python", "-m", "telegram_pymorphy_bot"]

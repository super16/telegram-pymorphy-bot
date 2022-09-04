FROM python:3.10.2-slim

WORKDIR /bot-app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /bot-app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python3", "-m", "telegram_pymorphy_bot"]

FROM python:3.10.2-slim
WORKDIR /bot-app
COPY . /bot-app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 80
ENV NAME App
CMD ["python3", "-m", "telegram_pymorphy_bot"]

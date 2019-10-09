FROM python:3.6-slim
WORKDIR /bot_app
COPY . /bot_app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 80
ENV NAME App
CMD ["python", "bot.py"]

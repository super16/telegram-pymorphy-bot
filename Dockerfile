FROM python:3.13-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /bot-app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ADD . /bot-app
RUN ["uv", "sync", "--locked"]

EXPOSE 80
CMD ["uv", "run", "python", "-m", "telegram_pymorphy_bot"]

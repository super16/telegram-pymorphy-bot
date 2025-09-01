# telegram-pymorphy-bot

Telegram Bot for linguistics morphology analysis. Reply with morphemes of
sent words and can suggest morphemes for unknown words. Works only with
russian language and reply with several variants of analysis if available.
Using awesome [pymorphy2](https://github.com/kmike/pymorphy2) module
with OpenCorpora corpus.

## Development mode

Requires [uv](https://docs.astral.sh/uv/).

### Install dependencies

```shell
uv sync
```

### Lint

```shell
uv run mypy telegram_pymorphy_bot
uv run ruff check telegram_pymorphy_bot --fix
```

### Run

```shell
TOKEN=<Telegram Bot Token> INFO="Add info to bot /info command" uv run python -m telegram_pymorphy_bot
```

## Docker

### Build

```bash
docker build --tag=pymorphy_bot .
```

### Run

```bash
docker run -d -e TOKEN=<Telegram Bot Token> -e INFO="Add info to bot /info command" pymorphy_bot
```

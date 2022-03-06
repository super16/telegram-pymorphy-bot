# telegram-pymorphy-bot

Telegram Bot for linguistics morphology analysis. Reply with morphemes of
sent words and can suggest morphemes for unknown words. Works only with
russian language and reply with several variants of analysis if available. 
Using awesome [pymorphy2](https://github.com/kmike/pymorphy2) module 
with OpenCorpora corpus.

## Development mode

```bash
pip3 install -r requirements.txt
TOKEN=<Telegram Bot Token> INFO="Add info to bot /info command" python3 -m telegram_pymorphy_bot
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

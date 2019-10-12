# Pymorphy2 Telegram Bot

Telegram [Bot](https://t.me/zaliznyak_bot) for linguistics morphology analysis. 
Reply with morphemes of sent words and can suggest morphemes for 
unknown words. Works only with russian language and reply with several 
variants of analysis if available. 
Using awesome [pymorphy2](https://github.com/kmike/pymorphy2) module 
with OpenCorpora corpus.

### Install with Docker

```
sudo docker build --tag=pymorphy_bot .
```
### Running Docker 

```
sudo docker run -d -e TOKEN=<Telegram Bot Token> -e INFO=<Add Info to Bot /info Command> pymorphy_bot
```


import os
from tags import grammems, unacceptable, analogies
import pymorphy2
import nltk
from telegram.ext import Updater, CommandHandler, MessageHandler

"""Telegram Bot for linguistics morphology analysis. Reply with 
morphemes of sent words and can suggest morphemes for unknown words. 
Works only with russian language and reply with several variants of 
analysis if available. Using awesome pymorphy2 module 
(https://github.com/kmike/pymorphy2) with OpenCorpora corpus"""

# Language Processing 
nltk.download("punkt")
morph = pymorphy2.MorphAnalyzer()

def gram(p, gr):
    """Generating a string with morphemes to reply"""
    f = ''
    for method in p.methods_stack:
        for m in method:
            for analogy_method in analogies:
                if analogy_method in str(m):
                    f = "<i>предположительный разбор:</i> "
    for k, v in grammems.items():
        if k in p.tag:
            gr.append(v)
    answer = "<b>" + p.word + "</b>" + " (" + f + ", ".join(gr) + ")"
    return answer


def analysis(update, context):
    """Processing input text (truncate everything over 64 characters
    and don't let incomplete words)"""
    tokens = nltk.word_tokenize(update.message.text)
    new_tokens = []
    for token in tokens:
        new_tokens.append(token)
        if sum(len(n) for n in new_tokens) > 64:
            new_tokens.pop()
            break
        else:
            pass
    if len(new_tokens) == 0:
        update.message.reply_text("Не удалось обработать текст")
    else:
        for word in new_tokens:
            parse = morph.parse(word)
            for p in parse:
                grammems_list = []
                if str(p.tag) in unacceptable:
                    pass
                elif len(word) == 1:
                    update.message.reply_text(gram(p, grammems_list), 
                    parse_mode='HTML')
                    break
                else:
                    update.message.reply_text(gram(p, grammems_list), 
                    parse_mode='HTML')

# Telegram Functions

def start(update, context):
    """/start command in bot"""
    update.message.reply_text("Введите слово или текст для \
    морфологического анализа")

def info(update, context):
    """/help command in bot"""
    update.message.reply_text(os.environ['INFO'], parse_mode='HTML')

def main():
    """Bot backend"""
    updater = Updater(os.environ['TOKEN'], 
    use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(MessageHandler(None, analysis))
    updater.start_polling()
    
if __name__ == "__main__":
    main()

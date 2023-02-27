from json import load
from logging import error
from os import environ
from typing import Dict, List, Optional, Tuple

from nltk import download, word_tokenize
from pymorphy3 import MorphAnalyzer
from pymorphy3.analyzer import Parse
from telegram import Chat, Message, Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
)
from telegram.ext.filters import COMMAND, TEXT


class Bot:
    """
    Telegram Bot for linguistics morphology analysis. Reply with
    morphemes of sent words and can suggest morphemes for unknown words.
    Works only with russian language and reply with several variants of
    analysis if available. Using awesome pymorphy2 module
    (https://github.com/kmike/pymorphy2) with OpenCorpora corpus.
    """

    # Methods of analogy analysis
    ANALOGIES: Tuple[str, ...] = (
        "KnownPrefixAnalyzer",
        "KnownSuffixAnalyzer",
        "FakeDictionary",
        "UnknownPrefixAnalyzer",
        "HyphenAdverbAnalyzer",
        "HyphenSeparatedParticleAnalyzer",
        "HyphenatedWordsAnalyzer"
    )

    # Words with unacceptable tags are not analysed
    UNACCEPTABLE: Tuple[str, ...] = (
        "LATN",
        "PNCT",
        "NUMB",
        "NUMB,intg",
        "NUMB,real",
        "ROMN",
        "UNKN"
    )

    def __init__(self) -> None:
        """
        Inits Bot with grammems const from JSON-file
        and MorphAnalyzer class instance from pymorphy2.
        """

        # Collections of tags from OpenCorpora
        # (http://opencorpora.org/dict.php?act=gram)
        #  with readable meaning in Russian to reply
        with open("telegram_pymorphy_bot/grammems.json", "r") as json_file:
            self.GRAMMEMS: Dict[str, str] = load(json_file)

        self.morph: MorphAnalyzer = MorphAnalyzer()

        self.application: Application = ApplicationBuilder().token(
            environ['TOKEN']
        ).build()

    async def analyze(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """
        Input text handler for morphological analysis.

        At first processing input text (truncate everything over
        64 characters and don't let incomplete words).

        Args:
          update:
            An incoming update instance.
          context:
            Context object passed to the callback.
        """

        update_message: Optional[Message] = None
        message_text: Optional[str] = ""

        if hasattr(update, "message"):
            update_message = update.message

        if update_message and hasattr(update_message, "text"):
            message_text = update_message.text

        tokens: List[str] = word_tokenize(message_text, language="russian")
        truncated_tokens: List[str] = []
        characters_count: int = 0

        for token in tokens:
            characters_count += len(token)
            if characters_count > 64:
                break
            else:
                if token not in truncated_tokens:
                    truncated_tokens.append(token)

        # Empty input
        if not truncated_tokens:
            await self.send_message(
                context, update, "Не удалось обработать текст",
            )
        else:
            for word in truncated_tokens:
                parse_results: List[Parse] = self.morph.parse(word)
                for p_result in parse_results:
                    grammems_list: List[str] = []
                    if str(p_result.tag) in self.UNACCEPTABLE:
                        pass
                    elif len(word) == 1:
                        # Weird fallback for one-letter words
                        await self.send_message(
                            context,
                            update,
                            self.generate_reply(p_result, grammems_list),
                        )
                        break
                    else:
                        await self.send_message(
                            context,
                            update,
                            self.generate_reply(p_result, grammems_list),
                        )

    async def info(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """
        Command handler /info callback in Telegram bot.

        Args:
          update:
            An incoming update instance.
          context:
            Context object passed to the callback.
        """
        await self.send_message(context, update, environ['INFO'])

    def generate_reply(
        self, parse_result: Parse, grammems_list: list
    ) -> str:
        """
        Generating a string with morphemes to reply.

        Args:
          parse_result: Parse object with morphological categories.
          grammems_list: Empty list to store found grammems.

        Returns:
          A reply string with found grammems and label
          that analysis is presumptive.
        """
        proposal: str = ''

        for method in parse_result.methods_stack:
            if method[0].__class__.__name__ in self.ANALOGIES:
                proposal = "<i>предположительный разбор:</i> "

        for key, value in self.GRAMMEMS.items():
            if key in parse_result.tag:
                grammems_list.append(value)

        return (
            f"<b>{parse_result.word}</b> ({proposal}"
            f"{', '.join(grammems_list)})"
        )

    async def send_message(
        self,
        context: ContextTypes.DEFAULT_TYPE,
        update: Update,
        message: str
    ) -> None:

        chat: Optional[Chat] = None
        chat_id: Optional[int] = None
        if hasattr(update, "effective_chat"):
            chat = update.effective_chat

        if chat and hasattr(chat, "id"):
            chat_id = chat.id

        if chat and chat_id:
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    parse_mode="HTML",
                    text=message,
                )
            except Exception as e:
                error(e)

    async def start(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """
        Command handler /start callback in Telegram bot.

        Args:
          update:
            An incoming update instance.
          context:
            Context object passed to the callback.
        """
        await self.send_message(
            context,
            update,
            "Введите слово или текст для морфологического анализа"
        )

    def run(self) -> None:
        """
        Method to run bot and poll the requests.
        """
        # Add handlers
        self.application.add_handler(
            CommandHandler("start", self.start),
        )
        self.application.add_handler(
            CommandHandler("info", self.info),
        )
        self.application.add_handler(
            MessageHandler(TEXT & (~COMMAND), self.analyze),
        )

        # Start polling
        self.application.run_polling()


if __name__ == "__main__":
    # Get Punkt tokenizer models
    download("punkt")
    telegram_bot = Bot()
    telegram_bot.run()

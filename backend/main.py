import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from emoji import emojize

from horoscope import get_today_horoscope

ZODIAC_SIGNS_MAP = {
    "Овен " + emojize(":ram:", use_aliases=True): "aries",
    "Телец " + emojize(":water_buffalo:", use_aliases=True): "taurus",
    "Близнецы " + emojize(":two_women_holding_hands:", use_aliases=True): "gemini",
    "Рак " + emojize(":cancer:", use_aliases=True): "cancer",
    "Лев " + emojize(":leopard:", use_aliases=True): "leo",
    "Дева " + emojize(":dancer:", use_aliases=True): "virgo",
    "Весы " + emojize(":libra:", use_aliases=True): "libra",
    "Скорпион " + emojize(":scorpius:", use_aliases=True): "scorpio",
    "Стрелец " + emojize(":sagittarius:", use_aliases=True): "sagittarius",
    "Козерог " + emojize(":capricorn:", use_aliases=True): "capricorn",
    "Водолей " + emojize(":sweat_drops:", use_aliases=True): "aquarius",
    "Рыбы " + emojize(":tropical_fish:", use_aliases=True): "pisces",
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Я Мистер Мисикс, посмотрите на меня!"
    )

    help_command(update, context)


def horoscope(update: Update, context: CallbackContext) -> None:
    keyboard = []
    button_bucket_size = 2

    for i in range(0, len(ZODIAC_SIGNS_MAP), button_bucket_size):
        bucket = [
            InlineKeyboardButton(key, callback_data=ZODIAC_SIGNS_MAP[key])
            for key in list(ZODIAC_SIGNS_MAP.keys())[i:i + button_bucket_size]
        ]
        keyboard.append(bucket)

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выбери свой знак зодиака:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    logger.info(f"Receive answer: {query.data}")
    logger.info(f"From User: {query.from_user}")
    horoscope_data = get_today_horoscope(query.data)

    query.edit_message_text(text=horoscope_data)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f"""
        Доступные команды:
        
        /horoscope - узнай что ждет тебя сегодня! {emojize(":dizzy:", use_aliases=True)}
        """
    )


def _main():
    bot = Bot(
        token=os.environ.get('TELEGRAM_BOT_TOKEN'),
    )
    updater = Updater(bot=bot)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('horoscope', horoscope))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    _main()

#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import logging
import os
import requests
from dotenv import load_dotenv
from telegram import __version__ as TG_VER

load_dotenv()

TOKEN = os.environ.get("TOKEN")
hostname = os.environ.get("SERVER_IP")
SERVER_STATUS_MSG = os.environ.get("SERVER_STATUS_MSG")
SERVER_ERR_STATUS_MSG = os.environ.get("SERVER_ERR_STATUS_MSG")
KB_SERVER_MSG = os.environ.get("KB_SERVER_MSG")
F_PATH = os.environ.get("F_PATH")
F_MSG = os.environ.get("F_MSG")
KB_F_MSG = os.environ.get("KB_F_MSG")
F_ERR_MSG = os.environ.get("F_ERR_MSG")

S_PATH = os.environ.get("S_PATH")
S_MSG = os.environ.get("S_MSG")
S_ERR_MSG = os.environ.get("S_ERR_MSG")
KB_S_MSG = os.environ.get("KB_S_MSG")

CHAT_ID = os.environ.get("CHAT_ID")
NOTIFY_SERVER_ERR = os.environ.get("NOTIFY_SERVER_ERR")
NOTIFY_SERVER =  os.environ.get("NOTIFY_SERVER")
NOTIFY_F_ERR = os.environ.get("NOTIFY_F_ERR")
NOTIFY_S_ERR = os.environ.get("NOTIFY_S_ERR")

KB_CATALOG_MSG = os.environ.get("KB_CATALOG_MSG")
CATALOG_MSG = os.environ.get("CATALOG_MSG")

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if os.path.exists(f"{F_PATH}"):
        f_check = F_MSG
    else:
        f_check = F_ERR_MSG

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={NOTIFY_F_ERR}"
        print(requests.get(url).json()) # this sends the message        

    if os.path.exists(f"{S_PATH}"):
        s_check = S_MSG
    else:
        s_check = S_ERR_MSG

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={NOTIFY_S_ERR}"
        print(requests.get(url).json()) # this sends the message

    # hostname = "{SERVER_IP}"
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = text=f"{SERVER_STATUS_MSG}"
    else:
        pingstatus = text=f"{SERVER_ERR_STATUS_MSG}"
        
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton(KB_SERVER_MSG, callback_data=f"{pingstatus}"),
            InlineKeyboardButton(KB_F_MSG, callback_data=f"{f_check}"),
        ],
        [
            InlineKeyboardButton(KB_S_MSG, callback_data=f"{s_check}"),
            InlineKeyboardButton(KB_CATALOG_MSG, callback_data=f"{CATALOG_MSG}"),


        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("------- !!Aplicação em testes!! -------\nQual serviço você quer que eu verifique?", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"{query.data}")


async def catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Catalogo: https://news.gcampos.site/catalogo-plex.html")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /lullybot para utilizar este bot.")

async def criador_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Quem me criou foi o Glaucio Campos.")

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

#    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("lully", start)) 
    application.add_handler(CommandHandler("lullybot", start))
    application.add_handler(CommandHandler("ajuda", help_command))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("catalogo", catalogo))
    application.add_handler(CommandHandler("criador", criador_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

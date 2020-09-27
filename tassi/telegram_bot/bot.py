from typing import Dict, Union
from datetime import datetime
import os

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from tassi.database.model import Ruta
from tassi.database.errors import InvalidEntry

from haversine import haversine		#Compute Haversine distance


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def store_location(user_id: int, m_id: int, position_data: Dict[str, Union[float, int]]):

    """
    Store the trayectory point and time (position_data) produced by an user (user_id) in a message (m_id)
    """

    if ("longitude" in position_data.keys()) and ("latitude" in position_data.keys()) and ("datetime" in position_data.keys()):
        correct_types = type(position_data.get("longitude")) == float
        correct_types = correct_types and type(position_data.get("latitude")) == float
        correct_types = correct_types and type(position_data.get("datetime")) == int
        if correct_types:
            ruta = Ruta.get_or_none(message = m_id)

            if ruta:
                ruta.trajectory.append(position_data)

                if len(ruta.trajectory) >= 2:
                    current_position = tuple( [position_data.get("longitude"), position_data.get("latitude")] )
                    previous_position = tuple( [ruta.trajectory[-2].get("longitude"), ruta.trajectory[-2].get("latitude")] )
                    ruta.distance += haversine( previous_position, current_position )
                    ruta.time += position_data.get("datetime") - ruta.trajectory[-2].get("datetime")

                ruta.save()
            else:
                Ruta.create(
                    user= user_id,
                    message = m_id,
                    date = datetime.now(),
                    trajectory = [position_data],
                    time = 0,
                    distance = 0.0,
                )
        else:
            raise InvalidEntry("Invalid type for position_data")
    else:
        raise InvalidEntry("latitude or longitude not in the keys")

def parser(data):
    """
    Parse data from the telegram updater
    """
    message_id = data.message_id
    user_id = data.chat.id 
    position = {
        "longitude": data.location.longitude,
        "latitude": data.location.latitude,
    }

    date = None
    try:
        date = data.edit_date
    except:
        date = data.date

    position["datetime"] = date

    return (message_id, user_id, position)

def handle_location(update, _):

    message = None

    if update.edited_message == None:
        message = update.message
    else:
        message = update.edited_message

    data = parser(message)
    store_location(*data)


def main():
    """Start the bot."""
    load_dotenv()
    TOKEN = os.environ.get("TOKEN")

    # Create the Updater and pass it your token and private key
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
     # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # On messages that include passport data call msg
    dp.add_handler(MessageHandler(Filters.location, handle_location))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()

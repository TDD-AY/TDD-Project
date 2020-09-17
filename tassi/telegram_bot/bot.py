from typing import Dict
from datetime import datetime
import os

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from tassi.database.model import Ruta
from tassi.database.errors import InvalidEntry


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def store_location(user_id: int, m_id: int, coordinates: Dict[str, float]):

    if ("longitude" in coordinates.keys()) and ("latitude" in coordinates.keys()):
        if type(coordinates.get("longitude")) == float and type(coordinates.get("latitude")) == float:
            ruta = Ruta.get_or_none(message = m_id)

            if ruta:
                ruta.trajectory.append(coordinates)

                if len(ruta.trajectory) > 2:
                    # Todo: Calculate  Haversine distante 
                    pass

                ruta.save()
            else:
                Ruta.create(
                    user= user_id, 
                    message = m_id, 
                    date = datetime.now(), 
                    trajectory = [coordinates],
                )
        else:
            raise InvalidEntry("Invalid type for coordinates")
    else:
        raise InvalidEntry("latitude or longitude not in the keys")

    

def main():
    """Start the bot."""
    
    TOKEN = os.environ.get("TOKEN")
    
    pass

if __name__ == '__main__':
    load_dotenv()
    main()
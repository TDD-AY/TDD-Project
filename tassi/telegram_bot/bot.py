from typing import Dict
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

def store_location(user_id: int, m_id: int, position_data: Dict[str, float]):

    """
    Store the trayectory point and time (position_data) produced by an user (user_id) in a message (m_id)
    """

    if ("longitude" in position_data.keys()) and ("latitude" in position_data.keys()) and ("time" in position_data.keys()):
        correct_types = type(position_data.get("longitude")) == float
        correct_types = correct_types and type(position_data.get("latitude")) == float
        correct_types = correct_types and type(position_data.get("time")) == int
        if correct_types:
            ruta = Ruta.get_or_none(message = m_id)

            if ruta:
                ruta.trajectory.append(position_data)

                if len(ruta.trajectory) >= 2:
                    current_position = tuple( [position_data.get("longitude"), position_data.get("latitude")] )
                    previous_position = tuple( [ruta.trajectory[-2].get("longitude"), ruta.trajectory[-2].get("latitude")] )
                    ruta.distance += haversine( previous_position, current_position )
                    ruta.time += position_data.get("time") - ruta.trajectory[-2].get("time")

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



def main():
    """Start the bot."""

    TOKEN = os.environ.get("TOKEN")

    pass

if __name__ == '__main__':
    load_dotenv()
    main()

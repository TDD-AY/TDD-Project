import os

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def store_location(coordinates):
    pass

def read_location(update, context):
    pass

def main():
    """Start the bot."""
    
    TOKEN = os.environ.get("TOKEN")
    
    pass

if __name__ == '__main__':
    load_dotenv()
    main()
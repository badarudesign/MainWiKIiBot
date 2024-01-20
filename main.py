import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the command handler for /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am a Wikipedia Bot. Send me a query like /search hello to get information.')

# Define the command handler for /search
def search(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if query:
        # Use the Wikipedia API
        api_url = f'https://wikipedia.apinepdev.workers.dev/?wiki={query}'
        response = requests.get(api_url)

        if response.status_code == 200:
            result = response.json()
            update.message.reply_text(result.get('summary', 'No information found.'))
        else:
            update.message.reply_text('Error fetching information from Wikipedia.')
    else:
        update.message.reply_text('Please provide a search query.')

def main() -> None:
  # Set up the Telegram Bot with your API token
  updater = Updater("6347294583:AAGbbc6CuP1o4oilqdIijUY4hHvJZcnn3dE")

  dp = updater.dispatcher

  # Add command handlers
  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("search", search))

  # Start the Bot
  updater.start_polling()
  updater.idle()

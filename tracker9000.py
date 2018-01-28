from telegram.ext import Updater, CommandHandler, ConversationHandler
import logging

from package_tracker import show_track

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# @tracker9000
TOKEN = open('token.txt').read()

# conversation states are defined below
TRACK = range(1)

def format_tracking_reply(track_results):
    date, event, office, location = track_results

    format_str = 'Data: {}\n'
    format_str += 'Eventi: {}\n'
    format_str += 'Zyra: {}'

    location = location.strip()
    if location != '':
        format_str += '\nVendndodhja: {}'
    return format_str.format(date, event, office, location)

def track(bot, update):
    tokenized_text = update.message.text.split()

    # sanity check
    if len(tokenized_text) <= 1:
        update.message.reply_text('Please enter your tracking number like so: /track AA000000000AA')
        return

    _, tracking_number = tokenized_text
    track_results = show_track(tracking_number)
    update.message.reply_text(format_tracking_reply(track_results))

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def start(bot, update):
    update.message.reply_text('sup noobs, use /track to track yo trackables')

def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('track', track))

    # log all errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

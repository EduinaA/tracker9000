from telegram.ext import Updater, CommandHandler, ConversationHandler
import logging
from threading import Timer
from entries import Entries
from package_tracker import show_track

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# @tracker9000
TOKEN = open('token.txt').read()

# conversation states are defined below
TRACK = range(1)

# interval to check for change
# CHECK_INTERVAL = 60 * 60 * 12 # in seconds
CHECK_INTERVAL = 10

# simulate check for changes
SIMULATION = True

entries = Entries()

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
    if len(tokenized_text) != 2:
        update.message.reply_text('Please enter your tracking number like so: /track AA000000000AA')
        return
    _, tracking_number = tokenized_text

    track_results = show_track(tracking_number)
    update.message.reply_text(format_tracking_reply(track_results))

def stop(bot, update):
    global entries
    tokenized_text = update.message.text.split()

    # sanity check
    if len(tokenized_text) != 2:
        update.message.reply_text('Please enter your tracking number like so: /track AA000000000AA')
        return
    _, tracking_number = tokenized_text
    chat_id = update.message.chat_id
    entries.delete(tracking_number, chat_id)
    update.message.reply_text('You have stopped tracking this number')

counter = 0
def check(bot):
    global entries
    global counter

    for entry_key, old_date in entries.read_all():
        tracking_number, chat_id = entry_key
        # check for changes in date
        track_results = show_track(tracking_number)
        new_date = track_results[0]

        # fake the new date if this is a simulation
        if SIMULATION:
            if counter % 2 == 0:
                new_date = '2018-02-11 3:00PM'
            else:
                new_date = '2018-02-12 3:00PM'
            counter += 1

        if new_date != old_date:
            # update the entry
            entries.update(tracking_number, chat_id, new_date)
            # notify the user
            message = 'Change detected\n'
            message += format_tracking_reply(track_results)
            bot.send_message(chat_id, message)

    timer = Timer(CHECK_INTERVAL, check, args=[bot])
    timer.start()


def notify(bot, update):
    """
    Subscribe to notifications for a given tracking number.
    Command format: /notify {tracking_number}
    :param bot: The bot object
    :param update: The update object when a user is requesting subscription
    :return:
    """
    global entries
    tokenized_text = update.message.text.split()

    # sanity check
    if len(tokenized_text) != 2:
        update.message.reply_text('Please enter your tracking number like so: /track AA000000000AA')
        return
    _, tracking_number = tokenized_text
    chat_id = update.message.chat_id
    # [ [chat_id, tracking_number, latest_date], array2, ..., arrayN]
    # { (chat_id, tracking_number): latest_date }
    track_results = show_track(tracking_number)
    latest_date = track_results[0]

    entries.add(tracking_number, chat_id, latest_date)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def start(bot, update):
    update.message.reply_text('sup noobs, use /track to track yo trackables')

def main():
    global entries

    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('track', track))
    dp.add_handler(CommandHandler('notify', notify))
    dp.add_handler(CommandHandler('stop', stop))

    check(updater.bot)

    # log all errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

import pickle

class Entries:
    def __init__(self):
        # entries filename
        self.filename = "entries.pickle"
        self.entries = {}
        self.load_from_disk()

    def load_from_disk(self):
        """ Loads JSON serialized state from 'filename' """
        try:
            file = open(self.filename, "rb")
            file_contents = file.read()
            file.close()
            self.entries = pickle.loads(file_contents)
        except FileNotFoundError as e:
            # return empty dictionary if file is non-existent
            pass

    def save_to_disk(self):
        """ Saves JSON serialized state to 'filename' """
        file = open(self.filename, "wb")
        file_contents = pickle.dumps(self.entries)
        file.write(file_contents)
        file.close()

    def add(self, tracking_number, chat_id, latest_date):
        self.update(tracking_number, chat_id, latest_date)

    def update(self, tracking_number, chat_id, latest_date):
        entry_key = (tracking_number, chat_id)
        self.entries[entry_key] = latest_date
        self.save_to_disk()

    def delete(self, tracking_number, chat_id):
        entry_key = (tracking_number, chat_id)
        del self.entries[entry_key]
        self.save_to_disk()

    def read_all(self):
        self.save_to_disk()
        entries_items = list(self.entries.items())
        return entries_items

import json

CONFIG_FILENAME = "config.json"


class ConfigManager(object):
    """ Control storage and access of application configuration through singleton type instance,
    This class controls saving and restoring of configuration also, config is held as key/value
    pairs and are stored in JSON format
    """
    def __init__(self):
        self.config = {}

    def get_config(self, key, default=None):
        if key in self.config:
            return self.config[key]
        else:
            return default

    def set_config(self, key, val):
        self.config[key] = val

    def save_config(self):
        with open(CONFIG_FILENAME, 'w') as outfile:
            json.dump(self.config, outfile, indent=2, sort_keys=True)

    def load_config(self):
        with open(CONFIG_FILENAME) as json_data_file:
            self.config = json.load(json_data_file)

configManager = ConfigManager()

import json

class Config:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self):
        """Loads config from JSON file."""
        with open(self.config_path, "r") as file:
            return json.load(file)

    def get(self, key, default=None):
        """Retrieves config values."""
        return self.config_data.get(key, default)


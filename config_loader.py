import json

class ConfigLoader:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path

    def load(self):
        """ Load configuration from a JSON file """
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Config file '{self.config_path}' not found.")
            raise
        except json.JSONDecodeError:
            print(f"❌ Error parsing config file '{self.config_path}'. Make sure it's valid JSON.")
            raise

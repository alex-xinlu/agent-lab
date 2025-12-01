import os
import json


def load_config(options):
    config_path = "config/config/config.json"

    config = None
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.loads(f.read())
    else:
        config = {}
    return config
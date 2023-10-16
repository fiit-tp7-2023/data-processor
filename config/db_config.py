import json

def get_db_config():
    with open('config/db_config.json', 'r') as config_file:
        db_config = json.load(config_file)
    return db_config
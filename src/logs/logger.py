import logging  
import json

class DataProcessingLogger:
    _instance = None
    log_file = None

    def __new__(cls, log_file):
        if cls._instance is None:
            cls._instance = super(DataProcessingLogger, cls).__new__(cls)
            cls._instance.init_logger(log_file)
        return cls._instance

    def init_logger(self, log_file):
        self.log_file = log_file
        logging.basicConfig(filename=log_file, level=logging.INFO)

    def get_instance():
        return DataProcessingLogger._instance

    def log(self, message):
        log_file = "src/logs/indexer_data/indexer.log"
        with open(log_file, 'a') as file:
            file.write(json.dumps(message) + '\n')

    def clear(self):
        log_file = "src/logs/indexer_data/indexer.log"
        with open(log_file, 'w') as file:
            file.write('')
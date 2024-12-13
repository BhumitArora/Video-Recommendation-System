import logging

# Set up logging
logging.basicConfig(filename="logs/app.log", level=logging.INFO, 
                    format="%(asctime)s - %(message)s")

def log_message(message):
    print(message)
    logging.info(message)

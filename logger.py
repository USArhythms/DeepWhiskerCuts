import logging
import os

def initiate_logger(folder):
    logging.basicConfig(filename=os.path.join(folder,'error.log'))

def log_error(path,step,exception):
    initiate_logger(path)
    logging.info(step)
    logging.error(exception, exc_info=True)
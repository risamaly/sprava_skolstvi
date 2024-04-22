import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),".."))
import logging


def setup_logger(name, log_file='log.log', level=logging.INFO, log_directory='LOG'):
    """Vytvoreni loggeru, ve stanovenem formatu"""
    
    log_path = os.path.join(log_directory, log_file)
    os.makedirs(log_directory, exist_ok=True)
    
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)

        file_handler = logging.FileHandler(log_path)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
    
    return logger

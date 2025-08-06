import logging
import os
from datetime import datetime

def setup_logger(name:str,filePath:str,level=logging.INFO)->logging.Logger:
    path = f"log/{filePath}"
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        os.makedirs(os.path.dirname(path),exist_ok=True)
        handler = logging.FileHandler(path)
        handler.setLevel(level)
        logger.addHandler(handler)
        logger.propagate = False

    return logger
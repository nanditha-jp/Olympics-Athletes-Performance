import logging

def configure_logger(name: str, log_file: str, log_level: str = "DEBUG") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.handlers:  # Prevent duplicate handlers
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setLevel("DEBUG")
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel("ERROR")
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

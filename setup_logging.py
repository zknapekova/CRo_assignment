import logging

def setup_logger(name: str, log_file_path: str):
    formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - [Line %(lineno)d in %(filename)s]: %(message)s",
                                        datefmt="%Y-%m-%d %H:%M:%S")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


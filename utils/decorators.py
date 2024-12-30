from logger import setup_logger


def log_execution(func):
    def wrapper(*args, **kwargs):
        logger = setup_logger()
        logger.info(f"Выполняется функция: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Функция {func.__name__} завершена")
        return result
    return wrapper

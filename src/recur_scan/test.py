from loguru import logger


def hello() -> None:
    """Log a hello world message.

    This function is a simple utility for testing logger configuration
    and verifying that the application's logging system is working correctly.

    Returns:
        None: This function doesn't return any value.

    Examples:
        >>> hello()
        # Logs "Hello, world!" at INFO level
    """
    logger.info("Hello, world!")

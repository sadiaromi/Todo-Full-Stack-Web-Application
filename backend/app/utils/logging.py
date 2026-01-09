import logging
from datetime import datetime
from typing import Optional

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)

def log_info(message: str, user_id: Optional[str] = None):
    """Log an info message with optional user context."""
    if user_id:
        logger.info(f"[USER:{user_id}] {message}")
    else:
        logger.info(message)

def log_error(message: str, user_id: Optional[str] = None, exception: Optional[Exception] = None):
    """Log an error message with optional user context and exception details."""
    if user_id:
        log_message = f"[USER:{user_id}] {message}"
    else:
        log_message = message

    if exception:
        logger.error(f"{log_message} | Exception: {str(exception)}")
    else:
        logger.error(log_message)

def log_warning(message: str, user_id: Optional[str] = None):
    """Log a warning message with optional user context."""
    if user_id:
        logger.warning(f"[USER:{user_id}] {message}")
    else:
        logger.warning(message)

def log_debug(message: str, user_id: Optional[str] = None):
    """Log a debug message with optional user context."""
    if user_id:
        logger.debug(f"[USER:{user_id}] {message}")
    else:
        logger.debug(message)
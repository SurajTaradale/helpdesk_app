import logging
import io
from datetime import datetime, timedelta
from threading import Timer

# Logger with in-memory stream and time tracking
log_stream = io.StringIO()
log_timestamps = []

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Check if the logger already has handlers
    if not logger.handlers:
        # Stream handler to capture logs in the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # In-memory handler for capturing logs in memory
        memory_handler = logging.StreamHandler(log_stream)
        memory_handler.setLevel(logging.ERROR)  # Set to capture only errors
        memory_handler.setFormatter(formatter)
        logger.addHandler(memory_handler)

    return logger

def log_cleaner():
    """
    Clears logs older than 30 minutes from the in-memory log stream.
    """
    global log_timestamps

    current_time = datetime.now()
    threshold_time = current_time - timedelta(minutes=30)

    # Identify logs older than 30 minutes
    to_remove = [i for i, timestamp in enumerate(log_timestamps) if timestamp < threshold_time]

    if to_remove:
        # Clear old logs
        log_stream.truncate(0)
        log_stream.seek(0)

        # Keep only the recent logs and timestamps
        log_timestamps = [timestamp for i, timestamp in enumerate(log_timestamps) if i not in to_remove]

    # Schedule the next cleaning in 30 minutes
    Timer(1800, log_cleaner).start()

# Start the log cleaner to run every 30 minutes
log_cleaner()

logger = get_logger(__name__)

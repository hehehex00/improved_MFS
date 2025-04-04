import logging

# Base log format
BASE_FORMAT = "[%(levelname)s | %(module)s | L%(lineno)d] %(asctime)s: %(message)s"

# Set up text colours based on the log level
FORMATS = {
    logging.DEBUG: BASE_FORMAT,
    logging.INFO: f"\33[36m{BASE_FORMAT}\33[0m",
    logging.WARNING: f"\33[33m{BASE_FORMAT}\33[0m",
    logging.ERROR: f"\33[31m{BASE_FORMAT}\33[0m",
    logging.CRITICAL: f"\33[1m\33[31m{BASE_FORMAT}\33[0m",
    logging.NOTSET: BASE_FORMAT,
}

class LogFormatter(logging.Formatter):
    """Initialize the LogFormatter class.

    This method initializes the LogFormatter class by calling the
    `__init__` method of the parent class `logging.Formatter`.

    Args:
    ----
    self (LogFormatter): An instance of the LogFormatter class.

    Returns:
    -------
    None

    """

    def __init__(self):
        """Initialize the LogFormatter class.

        This method initializes the LogFormatter class by calling the
        `__init__` method of the parent class `logging.Formatter`.

        Args:
        ----
        self (LogFormatter): An instance of the LogFormatter class.

        Returns:
        -------
        None

        """
        super().__init__()

    def format(self, record: logging.LogRecord):
        """Format the given log record according to the specified log level.

        Overrides the default format class.

        Args:
        ----
        record (logging.LogRecord): The log record to be formatted.

        Returns:
        -------
        str: The formatted log message.

        This method retrieves the appropriate log format based on the log level of
        the given record. It then uses the `logging.Formatter` class to format the
        record and returns the formatted log message.

        """
        log_fmt = FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, datefmt= "%Y-%m-%d %H:%M:%S %z")
        return formatter.format(record)

handler = logging.StreamHandler()
handler.setFormatter(LogFormatter())
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler],
)

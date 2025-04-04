import json
import logging
import logging.config
import logging.handlers
from pathlib import Path

from toolbox_logging.log_formatter import LogFormatter  # noqa: F401


def setup_logging():
    """Set up the logging configuration based on the provided JSON configuration file.

    Purpose:
    The function reads the JSON configuration file located at
        "logger_configs/config.json",
    loads its content, and then uses the dictConfig method from the logging module to
    apply the configuration to the custom logger.

    Usage:
    Call this function to initialize the logging configuration.
    """
    config_path = Path(__file__).parent / "logger_configs" / "config.json"
    try:
        with Path.open(config_path) as f_in:
            logger_config = json.load(f_in)
        log_file_path = Path(logger_config["handlers"]["file"]["filename"])
        log_dir_path = log_file_path.parent
        Path.mkdir(log_dir_path, exist_ok=True)
        logging.config.dictConfig(logger_config)
    except FileNotFoundError:
        print(f"Config file not found at: {config_path}")
    except Exception as e:  # noqa: BLE001
        print(f"Error loading logging configuration: {e}")

def main():
    """Initialize the logging configuration.

    Calls the setup_logging function to set up the logging configuration
    based on the provided JSON configuration file.

    Usage:
    Call this function to initialize the logging configuration.
    """
    setup_logging()

if __name__ == "__main__":
    main()

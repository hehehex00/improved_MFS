import json
import logging
from pathlib import Path

current_file_path = Path(__file__).parent.resolve()
styles_config_path = Path(f"{current_file_path}/styles.config.json")

logger = logging.getLogger("Toolbox")

def load_styles_config() -> dict:
    """Load the styles.config.json file."""
    try:
        with Path.open(styles_config_path) as styles:
            return json.loads(styles.read())
    except Exception:
        logger.exception("An error occurred while reading %s", styles_config_path)

def write_styles_config(styles_config: dict) -> None:
    """Update the styles.config.json file."""
    try:
        with Path.open(styles_config_path, "w") as styles:
            json.dump(styles_config, styles, indent=4)
    except Exception:
        logger.exception("An error occurred while writing to %s", styles_config_path)


import logging
from pathlib import Path


def setup_logging():
    """Configure application logging."""

    log_directory = Path("outputs")
    log_directory.mkdir(exist_ok=True)

    log_file = log_directory / "application.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True
    )

    logger = logging.getLogger("SmartChassis")

    logger.info("Logging system initialized")

    return logger


logger = setup_logging()
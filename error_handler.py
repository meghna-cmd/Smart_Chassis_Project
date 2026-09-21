
import logging
import traceback

logger = logging.getLogger("SmartChassis")


def handle_error(error, context="Unknown"):
    """Log errors and return a user-friendly message."""

    logger.error(
        "Error in %s: %s",
        context,
        str(error)
    )

    logger.debug(traceback.format_exc())

    return f"An error occurred in {context}. Please try again."


def safe_execute(function, context="Operation"):
    """Execute a function safely with error handling."""

    try:
        return function()

    except Exception as error:
        handle_error(error, context)
        return None
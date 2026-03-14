import json
import logging
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """
    Formatter class that formats log records into JSON strings.
    """

    def format(self, record):
        """
        Formats the log record into a JSON string.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The log record formatted as a JSON string.

        This function takes a log record and formats it into a JSON string. It starts
        by extracting the basic attributes from the record log. It then adds details
        about where the log originated from. It also includes optional fields provided
        in the 'extra' parameter of the log record. Finally, it formats any
        exceptions that occurred during the logging process.
        """
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # Tambahkan detail dari mana log berasal
        log_record.update(
            {
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            }
        )

        # extra data
        if hasattr(record, "extra_data"):
            log_record.update(record.extra_data)

        # exception format
        if record.exc_info:
            log_record["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }

        return json.dumps(log_record)


def setup_logger():
    """
    Set up a logger for the application.

    Returns:
        logging.Logger: The configured logger.
    """
    from app.core.config import settings

    logger = logging.getLogger("gunicorn.error")

    # Map string level from settings to logging integer constant safely
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)

    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

    return logger


class JsonLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        if "extra" in kwargs:
            kwargs["extra"] = {"extra_data": kwargs["extra"]}
        return msg, kwargs


# Initialize the logger
_logger = setup_logger()
json_logger = JsonLoggerAdapter(_logger, {})

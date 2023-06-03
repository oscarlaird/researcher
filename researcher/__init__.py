import logging
logging.basicConfig(level=logging.INFO)

# short python oneline to turn back on terminals linewrapping using ansi codes

'''
import os
class TruncatingFormatter(logging.Formatter):
    def format(self, record):
        terminal_width = os.get_terminal_size().columns
        message = super().format(record)
        return (message[:terminal_width - 4] + '...') if len(message) > terminal_width else message

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(TruncatingFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

'''

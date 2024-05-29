# custom_logging.py
import logging
import re
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class ColorFormatter(logging.Formatter):
    def format(self, record):
        log_colors = {
            'DEBUG': Fore.BLUE,
            'INFO': Fore.GREEN,
            'WARNING': Fore.YELLOW,
            'ERROR': Fore.RED,
            'CRITICAL': Fore.RED + Style.BRIGHT
        }

        levelname = record.levelname+""
        if levelname in log_colors:
            record.levelname = log_colors[levelname] + levelname + Style.RESET_ALL
            record.msg =  record.msg + Style.RESET_ALL

        return super().format(record)


class DefaultFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = remove_ansi(record.levelname)
        record.msg =  remove_ansi(record.msg)
        return super().format(record)

def remove_ansi(text):
  """Removes ANSI escape sequences from a string.

  Args:
      text: The string to remove ANSI codes from.

  Returns:
      The string without ANSI codes.
  """
  return re.sub(r'\x1b[^m]*m', '', text)
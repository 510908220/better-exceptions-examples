import logging
from better_exceptions import format_exception
class ExceptionFormatter(logging.Formatter):
    def formatException(self, ei):
        return format_exception(*ei)

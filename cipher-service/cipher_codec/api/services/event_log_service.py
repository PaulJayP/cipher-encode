import logging
import re

import bson

from common.models.event_log_object import EventLogObject
from common.services.queue_service import QueueService

logger = logging.getLogger("cipher-codec")


class EventLogService(object):
    """ Event log service - user to extract a log message,
    build this into an event object and send this to the
    event logging service via a rabbit mq queue.

    """

    def __init__(self):
        """ Initialize connection to queue service. """

        self.queue_service = QueueService()

    def event_log(self, message_log: str):
        """ Entry point into the event log service.
        Receives a message string, converts this to am EventLogObject and
        sends this to the queue service.

        :param message_log: The logged message string event.
        """

        bson_data = self.process_message_string_parser(message_log)

        self.queue_service.send_message(self.queue_service.MESSAGE_LOGGING_QUEUE, bson_data)

    def process_message_string_parser(self, err_message: str) -> bson:
        """ Parses message string using regex to find values using a set pattern.
        Inserts these values into the relative fields and builds the EventLogObject.

        :param err_message: The logged message string.
        :return: A BSON string object
        """

        log_object = EventLogObject()

        log_object.log_time = re.search(r'TIME: (?:\S)(?<=\[)(.*?)(?=,)', err_message).group(1)
        log_object.log_level = re.search(r'LEVEL: (?:\S)(?<=\[)(.*?)(?=\])]', err_message).group(1)
        log_object.log_module = re.search(r'MODULE: (?:\S)(?<=\[)(.*?)(?=\])]', err_message).group(1)
        log_object.log_function = re.search(r'FUNCTION: (?:\S)(?<=\[)(.*?)(?=\])]', err_message).group(1)
        log_object.log_message = re.search(r'MESSAGE: (?:\S)(?<=\[)(.*?)(?=\])]', err_message).group(1)

        return bson.dumps(log_object.to_dict())

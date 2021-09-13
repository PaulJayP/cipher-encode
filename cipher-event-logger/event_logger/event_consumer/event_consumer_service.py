import json
import logging
import sys
import threading
import traceback
from datetime import date
from pathlib import Path

import bson
from common.models.event_log_object import EventLogObject
from common.services.queue_service import QueueService

from logged_events import EVENT_STORAGE_PATH


class EventConsumerService(object):
    """ The Event Consumer Service -
    Connects to the given queue, consumes each event and
    (in lieu of a database) stores this within a valid directory/file.

    """

    EVENT_LOGGING_QUEUE = "event-logging"

    logger = logging.getLogger("cipher-event-logger")

    def __init__(self):
        """ Initialize Event Consumer class with object. """

        self.queue_service = self.connect()

    def connect(self):
        """ Initialises a connection to the RabbitMQ Service,
        and creates a consumer that attaches to the 'event-logging' Queue.

        :returns: A QueueService object.
        """

        self.queue_service = QueueService()

        self.queue_service.channel.basic_consume(
            queue=self.EVENT_LOGGING_QUEUE,
            on_message_callback=self.message_callback,
            consumer_tag=__name__
        )

        event_logging_thread = threading.Thread(
            target=self.queue_service.channel.start_consuming,
            name="event_logging_service_thread",
            daemon=True,
        )

        event_logging_thread.start()
        event_logging_thread.join(0)

        return self.queue_service

    def message_callback(self, ch, method, properties, message=None):
        """ Method called when an item is found on the event logging Queue. """

        try:
            self.logger.info(
                f"Event Logging Received Message : {message}"
            )
            self.consume_message(message)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.logger.error(
                "[Event logger callback Error: {0}]".format(
                    traceback.format_exception(
                        exc_type, exc_value, exc_traceback
                    )
                )
            )

        self.queue_service.send_ack_to_queue(ch, method)

    def consume_message(self, message_string):
        """ Consumes each message object, determines the type of event
        and stores this in the relative directory.

        :param message_string: A BSON string
        """

        self.logger.info(f'Logging events from other services.')

        event_log_obj: EventLogObject = EventLogObject().to_obj(dict_data=bson.loads(message_string))
        if event_log_obj.log_level == 'ERROR':
            self.process_log(
                event_directory_path=Path(EVENT_STORAGE_PATH, 'logged_errors'),
                event_type_file_name='ERROR LOG',
                event_log_object=event_log_obj
            )
        else:
            self.process_log(
                event_directory_path=Path(EVENT_STORAGE_PATH, 'logged_actions'),
                event_log_object=event_log_obj
            )

    def process_log(
        self,  event_log_object: EventLogObject,
        event_directory_path: Path, event_type_file_name='INFO'
    ):
        """ Processes each consumed Event object.
        Generates a file name using today's date and the event type.

        If the file exists, append to existing, else create a new file and add the data.

        :param event_log_object: An EventLogObject.
        :param event_directory_path: The directory Path object.
        :param event_type_file_name: The type of event.
        """

        current_date = date.today().strftime("%d-%m-%Y")

        file_name = '{0}-DATE={1}.log'.format(event_type_file_name, current_date)

        file_path_name = Path(event_directory_path, file_name)
        if file_path_name.exists():
            self.save_log(event_log_object, file_path_name=file_path_name, append_file=True)
        else:
            self.save_log(event_log_object, file_path_name=file_path_name)

    def save_log(
        self, event_log_object: EventLogObject,
        file_path_name, append_file=False
    ):
        """ Used to save the given Object to the file
        with the given directory path name.

        If `append_file=True` - append to existing,
        else create a new file and add the data.

        :param event_log_object: An EventLogObject.
        :param file_path_name: The full directory_file name.
        :param append_file: A boolean value.
        """

        if append_file is True:
            # Read json into python dict and modify
            with open(file_path_name, "r+") as file:
                data = json.load(file)
                data.append(event_log_object.to_dict())

            # Write json to file
            with open(file_path_name, "w") as file:
                json.dump(data, file, indent=4)
        else:
            with open(file_path_name, "w+") as file:
                json.dump([event_log_object.to_dict()], file, indent=4,)

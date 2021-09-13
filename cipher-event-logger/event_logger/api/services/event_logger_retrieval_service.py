import json
import logging
import os
from pathlib import Path

from logged_events import EVENT_STORAGE_PATH


class EventLoggerRetrievalService:
    """Event Logger Retrieval -
    Used as a data access service to find and return
    event log file and logged data.
    """

    logger = logging.getLogger("cipher-event-logger")

    def get_all_log_files(self, _path=EVENT_STORAGE_PATH,):
        """ Used to search each directory location recursively and build
        an array list of file names.

        :param _path: The path of the directory.
        :returns: A list of file names.
        """

        file_list = []
        self.logger.info('File path [{0}], file_list [{1}]'.format(_path, ', '.join(file_list)))
        for root, dirs, files in os.walk(_path):
            for file in files:
                if '__init__' not in file:
                    file_list.append(file)
        return file_list

    def get_all_logs_by_file_name(self,  file_name, _path=EVENT_STORAGE_PATH):
        """ Used to search for a file with a specific name.
        Loads the information within the file as a json object.

        :param file_name: The file name.
        :param _path: The directory path to search.
        :returns: A list of logged event as json.
        """

        for root, dirs, files in os.walk(_path):
            for sub_dir in dirs:
                sub_path = Path(EVENT_STORAGE_PATH, sub_dir, r'{0}'.format(file_name))
                try:
                    with open(sub_path, "r+") as file:
                        data = json.load(file)
                        return data
                except Exception as err:
                    pass

        else:
            raise Exception('File not found')

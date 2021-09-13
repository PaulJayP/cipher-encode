import json
import os
from pathlib import Path

from logged_events import EVENT_STORAGE_PATH


class EventLoggerRetrievalService:
    """Event Logger Retrieval -
    Used as a data access service to find and return
    event log file and logged data.
    """

    def get_all_log_files(self, _path=EVENT_STORAGE_PATH, file_list=[]):
        """ Used to search each directory location recursively and build
        an array list of file names.

        :param _path: The path of the directory.
        :param file_list: The list of file names.
        :returns: A list of file names.
        """

        for root, dirs, files in os.walk(_path):
            for sub_dir in dirs:
                if sub_dir != '__pycache__':
                    self.get_all_log_files(Path(EVENT_STORAGE_PATH, sub_dir), file_list=file_list)
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

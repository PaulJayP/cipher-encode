import json
import logging

from flask import Response
from flask_restx import Resource, Namespace

from event_logger.api.services.event_logger_retrieval_service import EventLoggerRetrievalService

logger = logging.getLogger("cipher-event-logger")

cipher_event_logger_api = Namespace(
    "cipher-event-logger", description="Event logger resource"
)


@cipher_event_logger_api.route("/")
class ListEventFilesResource(Resource):
    """ ListEventFiles resource - used to return all
    available Log data stored.
    """

    @cipher_event_logger_api.doc(
        responses={
            500: "Return if an internal server error has occurred",
            200: "List object payload successfully found and returned ",
        }
    )
    def get(self,):
        """ Finds and returns all available logged events.

        :return: A list of available event file names
        :status_code 500: Return if an Exception has occurred.
        """

        try:
            log_files = EventLoggerRetrievalService().get_all_log_files()

            return Response(
                json.dumps({"log_list": log_files}),
                mimetype='application/json',
                status=200
            )
        except Exception as err:
            return Response(
                {"message": str(err)},
                mimetype='application/json',
                status=500
            )


@cipher_event_logger_api.route("/<string:file_name>")
class ListEventsResource(Resource):
    """ ListEvents resource - used to return all
    available log data for a given file.
    """

    @cipher_event_logger_api.doc(
        responses={
            500: "Return if an internal server error has occurred",
            200: "Log file object list payload successfully found and returned",
        }
    )
    def get(self, file_name):
        """ Returns all available logged events for the given file name.

        :return: A list of available event logs.
        :status_code 500: Return if an Exception has occurred.
        """

        try:
            log_file_data = EventLoggerRetrievalService().get_all_logs_by_file_name(file_name)
            return Response(
                json.dumps({"log_file_data": log_file_data}),
                mimetype='application/json',
                status=200
            )
        except Exception as err:
            return Response(
                json.dumps({"message": str(err)}),
                mimetype='application/json',
                status=500
            )

import logging
import logging.config
import os
import yaml
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restx import Api

from healthcheck import HealthCheck, EnvironmentDump

from event_logger.api.resources.event_logger_resource import cipher_event_logger_api
from event_logger.event_consumer.event_consumer_service import EventConsumerService

logger = logging.getLogger("cipher-event-logger")


def configure_logging():
    """ Configures the python logger object.
    Reads any configuration data from a config yaml file.
    """

    with open(os.path.join("event_logger/configuration/log_configuration.yaml"), "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)


def create_app(debug=False):
    """ Creates/configures the flask the application.

    :returns: A configured Flask Application object.
    """

    app = Flask(__name__)
    ma = Marshmallow(app)
    app.config["ERROR_404_HELP"] = False
    CORS(app)
    api = Api(app)
    app.debug = debug

    api.add_namespace(cipher_event_logger_api)

    health = HealthCheck()

    envdump = EnvironmentDump()
    app.add_url_rule(
        "/healthcheck", "healthcheck", view_func=lambda: health.run()
    )
    app.add_url_rule(
        "/environment", "environment", view_func=lambda: envdump.run()
    )
    return app


def init_services():
    """ Initialise and configure services and queues """

    logger.info("Initialise services and queues")
    event_consumer_service = EventConsumerService()

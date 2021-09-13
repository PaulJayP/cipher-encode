import logging
import logging.config
import os
import yaml
from common import event_log_stream
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restx import Api

from healthcheck import HealthCheck, EnvironmentDump

from cipher_codec.api.resources.codec_resource import cipher_codec_api
from cipher_codec.api.services.event_log_service import EventLogService

logger = logging.getLogger("cipher-codec")


def configure_logging():
    """ Configures the python logger object.
    Reads any configuration data from a config yaml file.

    Sets any other default configuration.
    """

    with open(os.path.join("cipher_codec/configuration/log_configuration.yaml"), "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    # Add IO String log handler
    log_format = ('TIME: [%(asctime)s] : '
                  'LEVEL: [%(levelname)s] : '
                  'MODULE: [%(module)s] : '
                  'FUNCTION: [%(funcName)s] : '
                  'MESSAGE: [%(message)s]')

    log_formatter = logging.Formatter(log_format)

    log_handler = logging.StreamHandler(event_log_stream)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(log_formatter)
    logging.getLogger('cipher-codec').addHandler(log_handler)


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

    api.add_namespace(cipher_codec_api)

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

    event_log_service = EventLogService()

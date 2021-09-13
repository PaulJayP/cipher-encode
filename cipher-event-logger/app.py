
from event_logger.configuration.resource_configuration import (
    create_app, configure_logging, init_services,
)

configure_logging()

if __name__ == "__main__":
    init_services()
    app = create_app(debug=False)

    app.run(
        host="0.0.0.0", port='5002',
    )

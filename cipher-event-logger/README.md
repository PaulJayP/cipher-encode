# Cipher Event Logger

## Summary

This micro-service is designed to consume event messages from a Queue and
stores the event data based on type in the required directory/file.

Contains 2 API endpoints to retrieve all available files and all data within a specific file.


## Usage

### Launching

When run locally. Event Logger Service can be found running on  `localhost:5002`

### Usage

#### `/cipher-event-logger/`

Url example: `http://0.0.0.0:5002/cipher-event-logger/`

Accepted request types: GET

Returns: A list of available files.

####` /cipher-event-logger/<string:file_name>`

Url example: `http://0.0.0.0:5002/cipher-event-logger/file_1.log`

Accepted request types: GET

Returns: A list of logged json events.

# Cipher Encrypt Services

## Summary

This repo houses a collection of micro-services is designed to encrypt/decrpyt payload data
and log all events that occur on the api.

## Services

* Cipher Service: Encrypt/decrypt payload text data.
* Event Logger Service: Consume and log all incoming error, info events etc
* RabbitMQ: Exchange and Queue service. Contains an Event_logger queue.

## Usage

### Launching

The micro-services application run with docker.

Run the command: `docker-compose up` from this directory.

### Usage

For usage please see the README section for each service.

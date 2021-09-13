import pika


class QueueService(object):
    """ The QueueService -
    on init creates a connection, exchanges and queue.
    """

    EXCHANGE = "cipher"
    MESSAGE_LOGGING_QUEUE = "event-logging"
    RABBIT_DOMAIN = "cipher-rabbitmq"
    DEV_DOMAIN = 'localhost'

    def __init__(self):
        self.channel = self.connect_channel()
        self.init_queues()

    def connect_channel(self):
        """ Get a connection to the local RabbitMQ service. """

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                heartbeat=0,
                blocked_connection_timeout=300,
            )
        )
        channel = connection.channel()

        # Ensure 1 message is given and consumed
        # by the consumer at any one time.
        channel.basic_qos(prefetch_count=1)
        return channel

    def init_queues(self):
        """ Initialises the core queues and exchanges. """

        self.channel.exchange_declare(
            exchange=self.EXCHANGE, exchange_type="direct", durable=True
        )

        self.channel.queue_declare(self.MESSAGE_LOGGING_QUEUE, durable=True)

        self.channel.queue_bind(
            exchange=self.EXCHANGE, queue=self.MESSAGE_LOGGING_QUEUE
        )

    def send_message(self, name, content):
        """ Sends a message (content) to the named queue (name).

        :param name: The name of the queue to pass this object to.
        :param content: The object to pass.
        """

        self.channel.basic_publish(
            exchange=self.EXCHANGE,
            routing_key=name,
            body=content,
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def close_connection(self):
        """ Closes the channel connection. """

        self.channel.close()

    def send_ack_to_queue(self, channel, method):
        """ Method that sends an 'ack' (Acknowledgement) to the Queue.

        :param channel: The Current Connection Channel.
        :param method: The pika method object.
        """

        channel.basic_ack(delivery_tag=method.delivery_tag)

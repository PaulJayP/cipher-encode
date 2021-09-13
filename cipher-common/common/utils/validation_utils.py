from common.custom_exceptions.model_load_exceptions import FieldKeyForbiddenBytesSize


class ValidationUtils:
    """ Validation Utils - contains methods
    that can be used to validate fields or data."""

    ALLOWED_BYTE_LENGTH = [16, 24, 32]

    @classmethod
    def validate_key_length(cls, key):
        """ Validates the incoming key to ensure that it
        is AES_GCM compatible, within a range of 128, 192, 256
        bits respectively.

        :param key: The bytes key.
        :raises FieldKeyForbiddenBytesSize: An exception if key not valid.
        """

        if len(key) not in cls.ALLOWED_BYTE_LENGTH:
            raise FieldKeyForbiddenBytesSize(len(key))

from common.custom_exceptions.model_load_exceptions import FieldEmptyStringError
from common.utils.validation_utils import ValidationUtils


class CodecEncryptRequest:

    payload: bytes
    key: bytes

    def __init__(self, payload=None, key=None):
        try:
            self.payload = bytes(payload, encoding='utf-8')
            self.key = bytes(key, encoding='utf-8')
        except TypeError as err:
            raise FieldEmptyStringError(err)

        ValidationUtils.validate_key_length(self.key)

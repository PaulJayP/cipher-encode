import base64

from common.custom_exceptions.model_load_exceptions import FieldEmptyStringError
from common.utils.validation_utils import ValidationUtils


class CodecDecryptRequest:

    cipher_text: bytes
    key: bytes
    tag: bytes
    nonce: bytes

    def __init__(self, cipher_text=None, key=None, tag=None, nonce=None):
        try:
            self.cipher_text = base64.b64decode(cipher_text)
            self.tag = base64.b64decode(tag)
            self.nonce = base64.b64decode(nonce)
            self.key = bytes(key, encoding='utf-8')
        except TypeError as err:
            raise FieldEmptyStringError(err)

        ValidationUtils.validate_key_length(self.key)

from flask_apiexceptions import ApiException


class CodecDecryptionException(ApiException):

    status_code: int
    message: str
    error_args: any

    def __init__(self, error_args):
        super().__init__()
        self.status_code = 500
        self.message = "Error: Unable to verify decryption. Key incorrect or message corrupted."
        self.error_args = error_args

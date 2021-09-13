from flask_apiexceptions import ApiException


class FieldEmptyStringError(ApiException):

    status_code: int
    message: str
    error_args: any

    def __init__(self, error_args):
        super().__init__()
        self.status_code = 500
        self.message = "Error: Field missing string arg. Reason: {0}".format(
            error_args
        )
        self.error_args = error_args


class FieldKeyForbiddenBytesSize(ApiException):

    status_code: int
    message: str
    error_args: any

    def __init__(self, error_args):
        super().__init__()
        self.status_code = 500
        self.message = "Error: Key length is a forbidden byte size. Size must be 16, 24, or 32. " \
                       "Key byte size: [{0}]".format(error_args)
        self.error_args = error_args

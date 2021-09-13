import json
import logging

from common import event_log_stream
from common.custom_exceptions.codec_exceptions import CodecDecryptionException
from common.custom_exceptions.model_load_exceptions import FieldKeyForbiddenBytesSize, FieldEmptyStringError
from common.models.codec_decrypt_request import CodecDecryptRequest
from common.models.codec_decrypt_response import CodecDecryptResponse
from common.models.codec_encrypt_request import CodecEncryptRequest
from common.models.codec_encrypt_response import CodecEncryptResponse
from common.schemas.codec_decrypt_request_schema import codec_decrypt_request_schema
from common.schemas.codec_decrypt_response_schema import codec_decrypt_response_schema
from common.schemas.codec_encrypt_request_schema import codec_encrypt_request_schema
from common.schemas.codec_encrypt_response_schema import codec_encrypt_response_schema

from flask import request, Response
from flask_restx import Resource, Namespace
from marshmallow import ValidationError

from cipher_codec.api.services.codec_service import CodecService
from cipher_codec.api.services.event_log_service import EventLogService

logger = logging.getLogger("cipher-codec")

cipher_codec_api = Namespace(
    "cipher-codec", description="Codec resource"
)


@cipher_codec_api.route("/encrypt")
class EncryptResource(Resource):
    """ Encrypt resource - used to encrypt a payload with
     the given key.
     """

    @cipher_codec_api.doc(
        responses={
            500: "Return if an internal server error has occurred",
            200: "Object payload successfully encrypted",
        }
    )
    def post(self,):
        """ Receives an encrypt payload request. Transforms the included json
        object into a CodecEncryptRequest. Validates each deserialized fields.

        Executes the encrypt service and returns a CodecEncryptResponse object
        with base64 encoded data.

        :return: Encrypted - base64 encoded CodecEncryptResponse payload.
        :status_code 500: Return if an Exception has occurred.
        """

        try:
            codec_request: CodecEncryptRequest = codec_encrypt_request_schema.load(request.json)

            (cipher_text, tag, nonce) = CodecService().encrypt_payload(codec_request)

            encrypt_response = codec_encrypt_response_schema.dump(
                CodecEncryptResponse(cipher_text=cipher_text, tag=tag, nonce=nonce)
            )

            logger.info('Successfully encrypted text.')
            logged_message = event_log_stream.getvalue()
            EventLogService().event_log(message_log=logged_message)

            return Response(
                json.dumps(encrypt_response),
                mimetype='application/json',
                status=200
            )

        except ValidationError as validation_obj:
            # Schema error
            error_string = ''
            for key, val in validation_obj.messages.items():
                error_string += 'Field: [{0}]=Errors: [{1}]'.format(key, ', '.join(val))

            logger.error(error_string)
            logged_error = event_log_stream.getvalue()
            EventLogService().event_log(message_log=logged_error)

            return Response(
                json.dumps({"message": error_string}),
                mimetype='application/json',
                status=500
            )

        except (FieldKeyForbiddenBytesSize, FieldEmptyStringError) as error_obj:
            # Fields errors
            logger.error(error_obj.message)
            logged_error = event_log_stream.getvalue()
            EventLogService().event_log(message_log=logged_error)

            return Response(
                json.dumps({"message": error_obj.message}),
                mimetype='application/json',
                status=error_obj.status_code
            )

        except Exception as error_message:
            # Other generic exception
            logger.error(error_message)
            logged_error = event_log_stream.getvalue()
            EventLogService().event_log(message_log=logged_error)

            return Response(
                json.dumps({"message": error_message}),
                mimetype='application/json',
                status=500
            )


@cipher_codec_api.route("/decrypt")
class DecryptResource(Resource):
    """ Decrypt resource - used to decrypt a payload with
     required additional data.
     """

    @cipher_codec_api.doc(
        responses={
            500: "Return if an internal server error has "
                 "occurred due to incorrect or malformed data",
            200: "Object payload successfully encrypted",
        }
    )
    def post(self):
        """ Receives a decrypt request. Transforms the included json
        object into a CodecDecryptRequest. Validates each deserialized fields.

        Executes the decrypt service and returns the decrypted text.

        :return: Unencrypted plain text.
        :status_code 500: Return if an Exception has occured.
        """

        try:
            codec_decrypt_request: CodecDecryptRequest = codec_decrypt_request_schema.load(request.json)

            decrypted_text = CodecService().decrypt_payload(codec_decrypt_request)

            decrypt_response = codec_decrypt_response_schema.dump(
                CodecDecryptResponse(plain_text=decrypted_text)
            )

            logger.info('Successfully decrypted text.')
            logged_error = event_log_stream.getvalue()
            EventLogService().event_log(message_log=logged_error)

            return Response(
                json.dumps(decrypt_response),
                mimetype='application/json',
                status=200
            )

        except ValidationError as validation_obj:
            # Schema error
            error_string = ''
            for key, val in validation_obj.messages.items():
                error_string += 'Field: [{0}]=Errors: [{1}]'.format(key, ', '.join(val))

            logger.error(error_string)
            logged_error = event_log_stream.getvalue()
            EventLogService().event_log(message_log=logged_error)

            return Response(
                json.dumps({"message": error_string}),
                mimetype='application/json',
                status=500
            )
        except (FieldKeyForbiddenBytesSize, FieldEmptyStringError) as error_obj:
            # Fields errors
            logger.error(error_obj.message)
            logged_error = event_log_stream.getvalue()
            EventLogService().event_log(message_log=logged_error)

            return Response(
                json.dumps({"message": error_obj.message}),
                mimetype='application/json',
                status=error_obj.status_code
            )
        except CodecDecryptionException as error_obj:
            # Codec decrypt exception
            logger.error(error_obj.message)
            logged_error = event_log_stream.getvalue()
            EventLogService().event_log(message_log=logged_error)
            return Response(
                json.dumps({
                    "message": error_obj.message,
                    "plain_text": error_obj.error_args
                }),
                mimetype='application/json',
                status=error_obj.status_code
            )
        except Exception as error_message:
            # Other generic exception
            logger.error(error_message)
            logged_error = event_log_stream.getvalue()
            EventLogService().event_log(message_log=logged_error)

            return Response(
                json.dumps({"message": error_message}),
                mimetype='application/json',
                status=500
            )


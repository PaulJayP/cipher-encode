from marshmallow import Schema, fields, post_load

from common.models.codec_decrypt_response import CodecDecryptResponse


class CodecDecryptResponseSchema(Schema):
    """Schema for Codec Encrypt Response."""

    plain_text = fields.Str(required=True, error_messages={'required': 'Cipher Text cannot be null'})

    @post_load
    def make_codec_encrypt_response(self, data, **kwargs):
        """ Modify deserialization to return a Codec Response
        instead of default dict.

        :param data: Inbound CodecDecryptResponse as dict.
        :return: Codec Decrypt Response object.
        """

        return CodecDecryptResponse(**data)


codec_decrypt_response_schema = CodecDecryptResponseSchema()


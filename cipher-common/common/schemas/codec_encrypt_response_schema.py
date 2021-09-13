from marshmallow import Schema, fields, post_load

from common.models.codec_encrypt_response import CodecEncryptResponse


class CodecEncryptResponseSchema(Schema):
    """Schema for Codec Encrypt Response."""

    cipher_text = fields.Str(required=True, error_messages={'required': 'Cipher Text cannot be null'})
    tag = fields.Str(required=True, error_messages={'required': 'Tag cannot be null'})
    nonce = fields.Str(required=True, error_messages={'required': 'Nonce cannot be null'})

    @post_load
    def make_codec_encrypt_response(self, data, **kwargs):
        """ Modify deserialization to return a Codec Response
        instead of default dict.

        :param data: Inbound CodecEncryptResponse as dict.
        :return: Codec Response object.
        """

        return CodecEncryptResponse(**data)


codec_encrypt_response_schema = CodecEncryptResponseSchema()



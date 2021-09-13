from marshmallow import Schema, fields, post_load

from common.models.codec_decrypt_request import CodecDecryptRequest


class CodecDecryptRequestSchema(Schema):
    """Schema for Codec Decrypt Request."""

    cipher_text = fields.Str(required=True, error_messages={'required': 'Cipher Text cannot be null'})
    key = fields.Str(required=True, error_messages={'required': 'Key cannot be null'})
    tag = fields.Str(required=True, error_messages={'required': 'Tag cannot be null'})
    nonce = fields.Str(required=True, error_messages={'required': 'Nonce cannot be null'})

    @post_load
    def make_codec_decrypt_request(self, data, **kwargs):
        """ Modify deserialization to return a CodecDecryptRequest
        instead of default dict.

        :param data: Inbound CodecDecrypt Request as dict.
        :return: Codec Decrypt Request object.
        """

        return CodecDecryptRequest(**data)


codec_decrypt_request_schema = CodecDecryptRequestSchema()


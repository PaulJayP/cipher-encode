from marshmallow import Schema, fields, post_load, pre_load

from common.models.codec_encrypt_request import CodecEncryptRequest


class CodecEncryptRequestSchema(Schema):
    """Schema for Codec Encrypt Request."""

    payload = fields.Str(required=True, error_messages={'required': 'Payload cannot be null'})
    key = fields.Str(required=True, error_messages={'required': 'Payload.Key cannot be null'})

    @post_load
    def make_codec_encrypt_request(self, data, **kwargs):
        """ Modify deserialization to return a CodecEncryptRequest
        instead of default dict.

        :param data: Inbound Codec Request as dict.
        :return: Codec Request object.
        """

        return CodecEncryptRequest(**data)


codec_encrypt_request_schema = CodecEncryptRequestSchema()


from Crypto.Cipher import AES
from common.custom_exceptions.codec_exceptions import CodecDecryptionException
from common.models.codec_decrypt_request import CodecDecryptRequest
from common.models.codec_encrypt_request import CodecEncryptRequest


class CodecService:
    """ Codec Service - Contains methods that are used to
    encrypt/decrypt a payload using a given key and any another other
    required information.
    """

    def encrypt_payload(self, codec_encrypt_request_obj: CodecEncryptRequest):
        """ Encrypts a payload using AES with GCM mode.
        Requires the poyload text and a GCM valid key.

        :param codec_encrypt_request_obj: A CodecEncryptRequest object.
        :return: A tuple object containing 3 byte objects - the encrypted text,
                a generated tag object and the nonce used.
        """

        cipher = AES.new(codec_encrypt_request_obj.key, AES.MODE_GCM)

        # Create a default GCM compatible nonce key
        nonce = cipher.nonce
        cipher_text, tag = cipher.encrypt_and_digest(codec_encrypt_request_obj.payload)

        return cipher_text, tag, nonce

    def decrypt_payload(self, codec_decrypt_request_obj: CodecDecryptRequest):
        """ Decrypts a payload using AES with GCM mode.
        Requires the encrypted text, original key used and the previously generated nonce.
        Will use the generated tag to verify that the encrypted message has not been corrupted
        or the given is is correct.

        :param codec_decrypt_request_obj: A CodecDecryptRequest object.
        :return: A plain text decrypted string.
        """

        cipher = AES.new(codec_decrypt_request_obj.key, AES.MODE_GCM, nonce=codec_decrypt_request_obj.nonce)
        plain_text = cipher.decrypt(codec_decrypt_request_obj.cipher_text)
        try:
            cipher.verify(codec_decrypt_request_obj.tag)
            return plain_text
        except ValueError as err:
            raise CodecDecryptionException(error_args=str(err))

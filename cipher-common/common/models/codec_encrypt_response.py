import base64


class CodecEncryptResponse:

    cipher_text: str
    tag: str
    nonce: str

    def __init__(self, cipher_text=None, tag=None, nonce=None):
        self.cipher_text = base64.b64encode(cipher_text)
        self.tag = base64.b64encode(tag)
        self.nonce = base64.b64encode(nonce)

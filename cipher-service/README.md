# Cipher Service

## Summary

This micro-service is designed to encrypt or decrypt payload data using AES_GCM standard.

Contains 2 API endpoints to POST the cipher requests.


## Usage

### Launching

When run locally. Cipher Service can be found running on  `localhost:5001`

### Usage

#### Endpoint `/cipher-codec/encrypt`

Url example: `http://0.0.0.0:5001/cipher-codec/encrypt`

Accepted request types: POST

Request example
```json
{
    "payload": "Experience is the teacher of all things.",
    "key": "Sixteen byte key"
}
```

Response example
```json
{
    "cipher_text": "b8b2ym0SqVz1iK4nuv4Mggw9t5uE4Ikt9aPj8qFXq37Xv22nd+KcvA==",
    "tag": "3jG1BqvvnFoj5lnVqZJawg==",
    "nonce": "aVYvao1zIAdz6xV3nA2sEQ=="
}
```

Returns: An encrypted text string and additional metadata.

#### Endpoint `cipher-codec/decrypt`

Url example: `http://0.0.0.0:5001/cipher-codec/decrypt`

Accepted request types: POST

Request example
```json
{
    "cipher_text": "b8b2ym0SqVz1iK4nuv4Mggw9t5uE4Ikt9aPj8qFXq37Xv22nd+KcvA==",
    "tag": "3jG1BqvvnFoj5lnVqZJawg==",
    "nonce": "aVYvao1zIAdz6xV3nA2sEQ==",
    "key": "Sixteen byte key"
}
```

Response example
```json
{
    "plain_text": "Experience is the teacher of all things."
}
```

Returns: A decrypted string.

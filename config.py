secret_key = b'R\x8b\xd9\xe1\x97\x8e\x12\xd8\xdb\t\x8e\x7fg\xe1\x03\xc1'

CHALLENGE_DEFAULT_BYTE_LEN = 32
UKEY_DEFAULT_BYTE_LEN = 20

COSE_ALG_ES256 = -7
COSE_ALG_PS256 = -37
COSE_ALG_RS256 = -257

pubkey_credparams = [
    {
        "type": "public-key",
        "alg": COSE_ALG_ES256
    },
    {
        "type": "public-key", 
        "alg": COSE_ALG_RS256
    },
    {
        "type": "public-key",
        "alg": COSE_ALG_PS256
    }
]

rp = {
    "name": "A test site",
    "id": "test.com"
}
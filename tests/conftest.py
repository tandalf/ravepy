import base64
from Crypto.Cipher import DES3
import hashlib

import pytest

from ravepy.resources.auth import AuthDetails

@pytest.fixture(scope='module')
def sample_auth_details():
    return AuthDetails('FLWSECK-123456c59c8ef06749e6a72bc90e34a1-X',
        public_key='FLWPUBK-123456c59c8ef06749e6a72bc90e34a1-X')

@pytest.fixture()
def sample_request_data():
    return {
        'pub_key': 'FLWPUBK-123456c59c8ef06749e6a72bc90e34a1-X',
        'currency': 'USD',
        'country': 'NG',
    }

@pytest.fixture()
def sample_integrity_checksum(sample_auth_details, sample_request_data):
    sorted_parameter_values = []
    for key in sorted(sample_request_data.keys()):
        sorted_parameter_values.append(sample_request_data[key])

    plain_text = auth_details.secret_key + ''.join(sorted_parameter_values)
    #implementation details from official web api docs
    md5Key = hashlib.md5(auth_details.encryption_key.encode("utf-8")).digest()
    md5Key = md5Key + md5Key[0:8]

    blockSize = 8
    padDiff = blockSize - (len(plain_text) % blockSize)
    cipher = DES3.new(md5Key, DES3.MODE_ECB)

    new_plain_text = "{}{}".format(plain_text, "".join(chr(padDiff) * padDiff))
    return base64.b64encode(cipher.encrypt(new_plain_text))

from __future__ import absolute_import, unicode_literals

import pytest
import base64
from Crypto.Cipher import DES3
import hashlib

from ravepy.resources.auth import AuthDetails

@pytest.fixture(scope='module')
def auth_details():
    return AuthDetails('FLWSECK-123456c59c8ef06749e6a72bc90e34a1-X',
        public_key='FLWPUBK-123456c59c8ef06749e6a72bc90e34a1-X')

def test_get_encryption_key(auth_details):
    #implementation details from official web api docs
    seckey = auth_details.secret_key
    hashedseckey = hashlib.md5(seckey.encode("utf-8")).hexdigest()
    hashedseckeylast12 = hashedseckey[-12:]
    seckeyadjusted = seckey.replace('FLWSECK-', '')
    seckeyadjustedfirst12 = seckeyadjusted[:12]
    encryption_key = seckeyadjustedfirst12 + hashedseckeylast12

    #assert our implementation meets theirs
    assert auth_details.encryption_key == encryption_key

def test_encrypt_data(auth_details):
    plain_text = 'ioe98i3g5n9wpn5gw935thq93hpt48hq39848q34ijoiqj4jn4'
    #implementation details from official web api docs
    md5Key = hashlib.md5(auth_details.encryption_key.encode("utf-8")).digest()
    md5Key = md5Key + md5Key[0:8]

    blockSize = 8
    padDiff = blockSize - (len(plain_text) % blockSize)
    cipher = DES3.new(md5Key, DES3.MODE_ECB)

    new_plain_text = "{}{}".format(plain_text, "".join(chr(padDiff) * padDiff))
    encrypted = base64.b64encode(cipher.encrypt(new_plain_text))

    assert auth_details.encrypt_data(plain_text) == encrypted

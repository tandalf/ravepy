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

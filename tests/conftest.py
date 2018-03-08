import base64
from Crypto.Cipher import DES3
import hashlib

import pytest

from ravepy import constants
from ravepy.resources.auth import AuthDetails

@pytest.fixture(scope='module')
def sample_auth_details():
    return AuthDetails('FLWSECK-123456c59c8ef06749e6a72bc90e34a1-X',
        public_key='FLWPUBK-123456c59c8ef06749e6a72bc90e34a1-X',
        env='DEV')

@pytest.fixture()
def sample_request_data():
    return {
        'PBFPubKey': 'FLWPUBK-123456c59c8ef06749e6a72bc90e34a1-X',
        'currency': 'USD',
        'country': 'NG',
    }

@pytest.fixture()
def sample_original_request_data():
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

    plain_text = sample_auth_details.secret_key +\
        ''.join(sorted_parameter_values)
    blockSize = 8
    padDiff = blockSize - (len(plain_text) % blockSize)
    cipher = DES3.new(sample_auth_details.encryption_key, DES3.MODE_ECB)

    new_plain_text = "{}{}".format(plain_text, "".join(chr(padDiff) * padDiff))
    return base64.b64encode(cipher.encrypt(new_plain_text)).decode('utf-8')


#Integration tests
@pytest.fixture()
def partial_charge_request1():
    """
    Charge request kwargs that will contain most of the neccesary data that is
    needed to make a local card charge transaction.
    """
    return {
        'currency': constants.NGN,
        'country': constants.NIGERIA,
        'amount': '450',
        'email': 'tim@live.com',
        'phone_number': '08081111111',
        'first_name': 'Timothy',
        'last_name': 'Ebiuwhe',
        'ip_address': '103.238.105.185',
        'merchant_ref': 'MXX-ASC-4578',
        'device_fingerprint': '69e6b7f0sb72037aa8428b70fbe03986c'
    }

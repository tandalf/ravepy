from __future__ import absolute_import, unicode_literals
from random import randint

import pytest

import ravepy
from ravepy.constants import CARD
from ravepy.resources.auth import AuthDetails

@pytest.fixture()
def direct_mastercard_charge_with_pin(btn1_auth_details,
    partial_charge_request1, mastercard):
    ravepy.set_auth(btn1_auth_details)
    req_kwargs = {}
    req_kwargs.update(partial_charge_request1)
    req_kwargs.update(mastercard)
    otp = req_kwargs.pop('otp')
    pin = req_kwargs.pop('pin')
    return ravepy.Charge.create(source_type=CARD, **req_kwargs)

def test_direct_charge_mastercard_with_pin(direct_mastercard_charge_with_pin,
    mastercard):
    ch = direct_mastercard_charge_with_pin
    pin = mastercard['pin']
    ch.charge()
    print('charge_request_data')
    print(ch.charge_request_data)
    assert ch.charge_request_data['status'] == 'success'

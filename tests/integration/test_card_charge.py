from __future__ import absolute_import, unicode_literals
from random import randint

import pytest

import ravepy
from ravepy.constants import CARD
from ravepy.resources.auth import AuthDetails
from ravepy.exceptions.charge import RaveChargeError

@pytest.fixture()
def direct_mastercard_charge_with_pin(btn1_auth_details,
    partial_charge_request1, mastercard):
    ravepy.set_auth(btn1_auth_details)
    req_kwargs = {}
    req_kwargs.update(partial_charge_request1)
    req_kwargs.update(mastercard)
    otp = req_kwargs.pop('otp')
    #pin = req_kwargs.pop('pin')
    return ravepy.Charge.create(source_type=CARD, **req_kwargs)

@pytest.fixture()
def direct_mastercard_charge_without_pin(btn1_auth_details,
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
    ch.charge()
    assert ch.charge_response_data['status'] == 'success'

def test_direct_charge_mastercard_without_pin(
    direct_mastercard_charge_without_pin, mastercard):
    ch = direct_mastercard_charge_without_pin

    # confirm that without pin, an exception is raised except one is provided
    # when making the charge
    with pytest.raises(RaveChargeError):
        ch.charge()
    ch.charge(pin=mastercard['pin'])

    assert ch.charge_response_data['status'] == 'success'

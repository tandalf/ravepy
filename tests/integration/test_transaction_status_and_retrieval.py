from __future__ import absolute_import, unicode_literals

import pytest

import ravepy
from ravepy.resources.auth import AuthDetails
from ravepy.exceptions.charge import RaveChargeError
from ravepy.constants import CARD, DIRECT_CHARGE

def test_retrieve_mastercard(direct_mastercard_charge_with_pin,
    mastercard):
    ch = direct_mastercard_charge_with_pin
    ch.charge()
    auth_details = ch._auth_details
    gateway_ref = ch.charge_response_data['data']['flwRef']

    #perform the normal transation status retrieval
    ch = ravepy.Charge.retrieve(auth_details, charge_type=DIRECT_CHARGE,
        gateway_ref=gateway_ref, source_type=CARD)
    assert ch.was_retrieved == True
    assert ch.verification_response_data['data']['flw_ref'] == gateway_ref

def test_retrieve_mastercard_xrequery(direct_mastercard_charge_with_pin,
    mastercard):
    ch = direct_mastercard_charge_with_pin
    ch.charge()
    auth_details = ch._auth_details
    merchant_ref = ch.charge_response_data['data']['txRef']

    #perform the normal transation status retrieval
    ch = ravepy.Charge.retrieve(auth_details, charge_type=DIRECT_CHARGE,
        merchant_ref=merchant_ref, use_merchant_ref=True, source_type=CARD)
    assert ch.was_retrieved == True
    assert ch.verification_response_data['message'] == 'Tx Fetched'

def test_verify_mastercard(direct_mastercard_charge_with_pin):
    ch = direct_mastercard_charge_with_pin
    ch.charge()
    amount = ch.charge_request_data['amount']
    currency = ch.charge_request_data['currency']

    ch.verify(amount, currency)

def test_verify_mastercard_after_retrieve(direct_mastercard_charge_with_pin):
    ch = direct_mastercard_charge_with_pin
    ch.charge()
    auth_details = ch._auth_details
    gateway_ref = ch.charge_response_data['data']['flwRef']
    amount = ch.charge_request_data['amount']
    currency = ch.charge_request_data['currency']

    ch = ravepy.Charge.retrieve(auth_details, charge_type=DIRECT_CHARGE,
        gateway_ref=gateway_ref, source_type=CARD)
    ch.verify(amount, currency)

def test_verification_fails_when_amount_is_different(
    direct_mastercard_charge_with_pin):
    ch = direct_mastercard_charge_with_pin
    ch.charge()

    auth_details = ch._auth_details
    gateway_ref = ch.charge_response_data['data']['flwRef']
    amount = ch.charge_request_data['amount']
    currency = ch.charge_request_data['currency']

    # transaction amount should be AT LEAST the original amount
    with pytest.raises(RaveChargeError):
        ch.verify(amount-1.0, currency)
    ch.verify(amount+1.0, currency)

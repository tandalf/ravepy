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

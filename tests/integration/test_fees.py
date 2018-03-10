from __future__ import absolute_import, unicode_literals

import pytest

import ravepy
from ravepy import constants
from ravepy.exceptions.base import RaveError
from ravepy.resources.auth import AuthDetails
from ravepy.resources.fees import Fee

def test_list_fees(btn1_auth_details, mastercard):
    ravepy.set_auth(btn1_auth_details)
    fee = ravepy.Fee.get_fee(500, constants.NGN, card6=mastercard['cardno'][:6])
    print(fee)

    assert isinstance(fee, Fee)
    assert fee.charge_amount
    assert hasattr(fee, 'fee')

    # Confirm that accessing these does not raise
    fee.merchant_fee
    fee.rave_fee
    assert fee.raw_resp

def test_list_fees_with_invalid_ptype(btn1_auth_details):
    ravepy.set_auth(btn1_auth_details)
    with pytest.raises(RaveError):
        fee = ravepy.Fee.get_fee(500, constants.NGN, ptype='fer')

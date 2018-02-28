from __future__ import absolute_import, unicode_literals

import pytest

from ravepy.resources.auth import AuthDetails
from ravepy.exceptions.charge import RaveChargeError

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

def test_direct_charge_vervecard_with_pin(direct_vervecard_charge_with_pin,
    vervecard):
    ch = direct_vervecard_charge_with_pin
    ch.charge()
    assert ch.charge_response_data['status'] == 'success'

def test_direct_charge_visacard_intl_using_3dsecure(
    direct_visacard_charge_with_3dsecure, visacard):
    ch = direct_visacard_charge_with_3dsecure
    ch.charge()

    assert ch.charge_response_data['data']['authurl'].startswith('http')

from __future__ import absolute_import, unicode_literals

import pytest

from ravepy.resources.auth import AuthDetails
from ravepy.exceptions.charge import RaveChargeError

def test_error_mastercard_charge(error_mastercard_charge, mastercard):
    ch = error_mastercard_charge
    with pytest.raises(RaveChargeError,
        message='Charge request failed. See e.error_resp') as e:
        ch.charge()
        
    assert e.type == RaveChargeError
    assert e.value.error_resp['status'] == 'error'

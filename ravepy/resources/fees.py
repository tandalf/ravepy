from __future__ import absolute_import, unicode_literals
import json

from ravepy.utils.http import post
from ravepy.exceptions.base import RaveError, RaveGracefullTimeoutError
from ravepy.constants import ACCOUNT

__metaclass__ = type

class Fee:
    def __init__(self, auth_details, amount, currency, ptype=ACCOUNT, card6=None):
        self._auth_details = auth_details
        self._data = data

        self._amount = amount
        self._currency = currency
        self._ptype = ptype
        self._card6 = card6

    def get_fee(self):
        req_data = {
            'PBFPubKey': self._auth_details.public_key,
            'amount': self._amount,
            'currency': self._currency
        }
        if self._ptype:
            if self._ptype == ACCOUNT:
                req_data.update({'ptype': 2})
            else:
                raise RaveError('Invalid value for \'ptype\'. Must be ACCOUNT')

        if self._card6:
            req_data.update({'card6': card6})

        self._data = post(self._auth_details.urls.GET_FEES_URL, req_data)
        return self._data

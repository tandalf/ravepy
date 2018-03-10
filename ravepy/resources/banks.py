"""
This module contains resources for interacting with bank data that exists on
the rave gateway.
"""
from __future__ import absolute_import, unicode_literals

from ravepy.constants import NIGERIA
from ravepy.utils.http import get

__metaclass__ = type

class Bank:
    def __init__(self, bank_name, bank_code, internet_banking=False):
        """
        This class holds information about banks that can be used for Account
        charges.
        """
        self._bank_name = bank_name
        self._bank_code = bank_code
        self._internet_banking = internet_banking

    def __str__(self):
        return "<Bank> name: {}, code: {}, internet_banking: {}".format(
            self._bank_name, self._bank_code, self._internet_banking)

    @property
    def name(self):
        """The name of the bank"""
        return self._bank_name

    @property
    def code(self):
        """The code of the bank"""
        return self._bank_code

    @property
    def internet_banking(self):
        """Boolean indicating if the bank supports internet banking"""
        return self._internet_banking

class BankFactory:
    def __init__(self, auth_details):
        self._auth_details = auth_details

    def list(self, country=NIGERIA):
        """
        Retrieves a list of Banks that are available in a country. The default,
        and only country with banks as of now is Nigeria.
        """
        banks = []
        for bank_data in get(self._auth_details.urls.BANKS_URL):
            banks.append(Bank(
                bank_name=bank_data['bankname'],
                bank_code=bank_data['bankcode'],
                internet_banking=bank_data['internetbanking'],
            ))

        return banks

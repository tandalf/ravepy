"""
This module contains resources for interacting with bank data that exists on
the rave gateway.
"""
from __future__ import absolute_import, unicode_literals

from ravepy.constants import NIGERIA

__metaclass__ = type

class Bank:
    def __init__(self, bank_name, bank_code, internet_banking=False):
        """
        This class holds information about banks that can be used for Account
        charges.
        """
        self.bank_name = bank_name
        self.bank_code = bank_code
        self.internet_banking = internet_banking
        
    @classmethod
    def list(self, country=NIGERIA):
        """
        Retrieves a list of Banks that are available in a country. The default,
        and only country with banks as of now is Nigeria.
        """
        return []

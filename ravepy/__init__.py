from __future__ import absolute_import, unicode_literals

from ravepy.resources.charge import ChargeFactory
from ravepy.resources.banks import BankFactory
from ravepy.constants import CARD, ACCOUNT

__metaclass__ = type

Charge = ChargeFactory(None)
Bank = BankFactory(None)

def set_auth(auth_details):
    global Charge
    global Bank
    Charge._auth_details = auth_details
    Bank._auth_details = auth_details

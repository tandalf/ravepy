from __future__ import absolute_import, unicode_literals

from ravepy.resources.charge import ChargeFactory
from ravepy.resources.banks import BankFactory
from ravepy.resources.fees import FeeFactory
from ravepy.constants import CARD, ACCOUNT

__metaclass__ = type

Charge = ChargeFactory(None)
Bank = BankFactory(None)
Fee = FeeFactory(None)

def set_auth(auth_details):
    global Charge
    global Bank
    global Fee
    Charge._auth_details = auth_details
    Bank._auth_details = auth_details
    Fee._auth_details = auth_details

from __future__ import absolute_import, unicode_literals

from ravepy.resources.charge import ChargeFactory
from ravepy.constants import CARD, ACCOUNT

__metaclass__ = type

Charge = ChargeFactory(None)

def set_auth(auth_details):
    global Charge
    Charge._auth_details = auth_details

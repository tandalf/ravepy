from __future__ import absolute_import, unicode_literals

"""
Constants used in this library are found here. Majority are currency constants.
"""

#currencies
NGN = 'NGN'
USD = 'USD'
KES = 'KES'
EUR = 'EUR'
GBP = 'GBP'
GHS = 'GHS'
ZAR = 'ZAR'

#countries
NIGERIA = 'NG'
KENYA = 'KE'
GHANA = 'GH'
SOUTH_AFRICA = 'ZA'

COUNTRY_CURRENCIES = {
    NIGERIA: [NGN, USD, KES, EUR, GBP],
    KENYA: [KES],
    GHANA: [GHS, USD],
    SOUTH_AFRICA: [ZAR]
}

#Auth methods
PIN = 'PIN'
VBVSECURECODE = 'VBVSECURECODE'
AVS_VBVSECURECODE = 'AVS_VBVSECURECODE'

#Charge types
PRE_AUTH_CHARGE = 'preauth'
NORMAL_CHARGE = 'normal'

#source_type
CARD='CARD'
ACCOUNT='ACCOUNT'

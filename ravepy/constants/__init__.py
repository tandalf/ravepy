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

# Charge urls
DIRECT_CHARGE_URL = 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'\
    '/flwv3-pug/getpaidx/api/charge'
VALIDATE_CARD_CHARGE_URL = 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'\
    '/flwv3-pug/getpaidx/api/validatecharge'
VALIDATE_ACCOUNT_CHARGE_URL = 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.'\
    'com/flwv3-pug/getpaidx/api/validate'
TRANSACTION_VERIFICATION_URL = 'http://flw-pms-dev.eu-west-1.elasticbeanstalk'\
    '.com/flwv3-pug/getpaidx/api/verify'
TRANSACTION_VERIFICATION_XREQUERY_URL = 'http://flw-pms-dev.eu-west-1.'\
    'elasticbeanstalk.com/flwv3-pug/getpaidx/api/xrequery'
PREAUTH_CHARGE_URL = 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'\
    '/flwv3-pug/getpaidx/api/charge'
PREAUTH_CAPTURE_URL = 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'\
    '/flwv3-pug/getpaidx/api/capture'

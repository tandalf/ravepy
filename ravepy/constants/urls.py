from __future__ import absolute_import, unicode_literals
from collections import namedtuple

URLS = namedtuple('URLS', ['DIRECT_CHARGE_URL', 'VALIDATE_CARD_CHARGE_URL',
    'VALIDATE_ACCOUNT_CHARGE_URL', 'TRANSACTION_VERIFICATION_URL',
    'TRANSACTION_VERIFICATION_XREQUERY_URL', 'PREAUTH_CHARGE_URL',
    'PREAUTH_CAPTURE_URL', 'PREAUTH_VOID_URL', 'GET_FEES_URL', 'BANKS_URL'])

DEV_URL = 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'
PROD_URL = 'https://api.ravepay.co'

dev_urls = URLS(
    DIRECT_CHARGE_URL=DEV_URL + '/flwv3-pug/getpaidx/api/charge',
    VALIDATE_CARD_CHARGE_URL=DEV_URL + '/flwv3-pug/getpaidx/api/validatecharge',
    VALIDATE_ACCOUNT_CHARGE_URL=DEV_URL + '/flwv3-pug/getpaidx/api/validate',
    TRANSACTION_VERIFICATION_URL=DEV_URL + '/flwv3-pug/getpaidx/api/verify',
    TRANSACTION_VERIFICATION_XREQUERY_URL=DEV_URL + \
        '/flwv3-pug/getpaidx/api/xrequery',
    PREAUTH_CHARGE_URL=DEV_URL + '/flwv3-pug/getpaidx/api/charge',
    PREAUTH_CAPTURE_URL=DEV_URL + '/flwv3-pug/getpaidx/api/capture',
    PREAUTH_VOID_URL=DEV_URL + '/flwv3-pug/getpaidx/api/refundorvoid',
    GET_FEES_URL=DEV_URL + '/flwv3-pug/getpaidx/api/fee',
    BANKS_URL=DEV_URL + '/flwv3-pug/getpaidx/api/flwpbf-banks.js?json=1')






prod_urls = URLS(
    DIRECT_CHARGE_URL=PROD_URL + '/flwv3-pug/getpaidx/api/charge',
    VALIDATE_CARD_CHARGE_URL=PROD_URL + '/flwv3-pug/getpaidx/api/validatecharge',
    VALIDATE_ACCOUNT_CHARGE_URL=PROD_URL + '/flwv3-pug/getpaidx/api/validate',
    TRANSACTION_VERIFICATION_URL=PROD_URL + '/flwv3-pug/getpaidx/api/verify',
    TRANSACTION_VERIFICATION_XREQUERY_URL=PROD_URL + \
        '/flwv3-pug/getpaidx/api/xrequery',
    PREAUTH_CHARGE_URL=PROD_URL + '/flwv3-pug/getpaidx/api/charge',
    PREAUTH_CAPTURE_URL=PROD_URL + '/flwv3-pug/getpaidx/api/capture',
    PREAUTH_VOID_URL=PROD_URL + '/flwv3-pug/getpaidx/api/refundorvoid',
    GET_FEES_URL=PROD_URL + '/flwv3-pug/getpaidx/api/fee',
    BANKS_URL=PROD_URL + '/flwv3-pug/getpaidx/api/flwpbf-banks.js?json=1')

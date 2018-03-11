from __future__ import absolute_import, unicode_literals
from collections import namedtuple

URLS = namedtuple('URLS', ['DIRECT_CHARGE_URL', 'VALIDATE_CARD_CHARGE_URL',
    'VALIDATE_ACCOUNT_CHARGE_URL', 'TRANSACTION_VERIFICATION_URL',
    'TRANSACTION_VERIFICATION_XREQUERY_URL', 'PREAUTH_CHARGE_URL',
    'PREAUTH_CAPTURE_URL', 'PREAUTH_VOID_URL', 'GET_FEES_URL', 'BANKS_URL'])

DEV_URL = 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'
PROD_URL = 'https://api.ravepay.co'

url_kwargs = {
    'DIRECT_CHARGE_URL': '/flwv3-pug/getpaidx/api/charge',
    'VALIDATE_CARD_CHARGE_URL': '/flwv3-pug/getpaidx/api/validatecharge',
    'VALIDATE_ACCOUNT_CHARGE_URL': '/flwv3-pug/getpaidx/api/validate',
    'TRANSACTION_VERIFICATION_URL': '/flwv3-pug/getpaidx/api/verify',
    'TRANSACTION_VERIFICATION_XREQUERY_URL': '/flwv3-pug/getpaidx/api/xrequery',
    'PREAUTH_CHARGE_URL': '/flwv3-pug/getpaidx/api/charge',
    'PREAUTH_CAPTURE_URL': '/flwv3-pug/getpaidx/api/capture',
    'PREAUTH_VOID_URL': '/flwv3-pug/getpaidx/api/refundorvoi',
    'GET_FEES_URL': '/flwv3-pug/getpaidx/api/fee',
    'BANKS_URL': '/flwv3-pug/getpaidx/api/flwpbf-banks.js?json=1',
}

dev_url_kwargs = {}
prod_url_kwargs = {}

for url_name, url in url_kwargs:
    dev_url_kwargs[url_name] = DEV_URL + url
    prod_url_kwargs[url_name] = PROD_URL + url

dev_urls = URLS(**dev_url_kwargs)
prod_urls = URLS(**prod_url_kwargs)

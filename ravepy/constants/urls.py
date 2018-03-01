from collections import namedtuple

URLS = namedtuple('URLS', ['DIRECT_CHARGE_URL', 'VALIDATE_CARD_CHARGE_URL',
    'VALIDATE_ACCOUNT_CHARGE_URL', 'TRANSACTION_VERIFICATION_URL',
    'TRANSACTION_VERIFICATION_XREQUERY_URL', 'PREAUTH_CHARGE_URL',
    'PREAUTH_CAPTURE_URL'])

dev_urls = URLS(
    DIRECT_CHARGE_URL='http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'\
    '/flwv3-pug/getpaidx/api/charge',
    VALIDATE_CARD_CHARGE_URL='http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'\
        '/flwv3-pug/getpaidx/api/validatecharge',
    VALIDATE_ACCOUNT_CHARGE_URL='http://flw-pms-dev.eu-west-1.elasticbeanstalk.'\
        'com/flwv3-pug/getpaidx/api/validate',
    TRANSACTION_VERIFICATION_URL='http://flw-pms-dev.eu-west-1.elasticbeanstalk'\
        '.com/flwv3-pug/getpaidx/api/verify',
    TRANSACTION_VERIFICATION_XREQUERY_URL='http://flw-pms-dev.eu-west-1.'\
        'elasticbeanstalk.com/flwv3-pug/getpaidx/api/xrequery',
    PREAUTH_CHARGE_URL='http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'\
        '/flwv3-pug/getpaidx/api/charge',
    PREAUTH_CAPTURE_URL='http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'\
        '/flwv3-pug/getpaidx/api/capture',
    GET_FEES_URL='http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'\
        '/flwv3-pug/getpaidx/api/fee')






prod_urls = URLS(
    DIRECT_CHARGE_URL='http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'\
    '/flwv3-pug/getpaidx/api/charge',
    VALIDATE_CARD_CHARGE_URL='http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'\
        '/flwv3-pug/getpaidx/api/validatecharge',
    VALIDATE_ACCOUNT_CHARGE_URL='http://flw-pms-dev.eu-west-1.elasticbeanstalk.'\
        'com/flwv3-pug/getpaidx/api/validate',
    TRANSACTION_VERIFICATION_URL='http://flw-pms-dev.eu-west-1.elasticbeanstalk'\
        '.com/flwv3-pug/getpaidx/api/verify',
    TRANSACTION_VERIFICATION_XREQUERY_URL='http://flw-pms-dev.eu-west-1.'\
        'elasticbeanstalk.com/flwv3-pug/getpaidx/api/xrequery',
    PREAUTH_CHARGE_URL='http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'\
        '/flwv3-pug/getpaidx/api/charge',
    PREAUTH_CAPTURE_URL='http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'\
        '/flwv3-pug/getpaidx/api/capture')

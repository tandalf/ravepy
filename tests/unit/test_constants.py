from __future__ import absolute_import, unicode_literals

import pytest

import ravepy
from ravepy.constants.urls import dev_urls, prod_urls

def test_url_constants():
    assert getattr(dev_urls, 'DIRECT_CHARGE_URL', False)
    assert getattr(prod_urls, 'DIRECT_CHARGE_URL', False)
    assert getattr(dev_urls, 'VALIDATE_CARD_CHARGE_URL', False)
    assert getattr(prod_urls, 'VALIDATE_CARD_CHARGE_URL', False)
    assert getattr(dev_urls, 'VALIDATE_ACCOUNT_CHARGE_URL', False)
    assert getattr(prod_urls, 'VALIDATE_ACCOUNT_CHARGE_URL', False)
    assert getattr(dev_urls, 'TRANSACTION_VERIFICATION_URL', False)
    assert getattr(prod_urls, 'TRANSACTION_VERIFICATION_URL', False)
    assert getattr(dev_urls, 'TRANSACTION_VERIFICATION_XREQUERY_URL', False)
    assert getattr(prod_urls, 'TRANSACTION_VERIFICATION_XREQUERY_URL', False)
    assert getattr(dev_urls, 'PREAUTH_CHARGE_URL', False)
    assert getattr(prod_urls, 'PREAUTH_CHARGE_URL', False)
    assert getattr(dev_urls, 'PREAUTH_CAPTURE_URL', False)
    assert getattr(prod_urls, 'PREAUTH_CAPTURE_URL', False)
    assert getattr(dev_urls, 'PREAUTH_VOID_URL', False)
    assert getattr(prod_urls, 'PREAUTH_VOID_URL', False)
    assert getattr(dev_urls, 'GET_FEES_URL', False)
    assert getattr(prod_urls, 'GET_FEES_URL', False)
    assert getattr(dev_urls, 'BANKS_URL', False)
    assert getattr(prod_urls, 'BANKS_URL', False)

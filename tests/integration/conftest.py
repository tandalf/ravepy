import os

import pytest

import ravepy
from ravepy.constants import VBVSECURECODE, CARD
from ravepy.resources.auth import AuthDetails

@pytest.fixture()
def mastercard():
    return {
        'cardno': '5438898014560229',
        'cvv': '789',
        'expiry_month': '09',
        'expiry_year': '19',
        'pin': '3310',
        'otp': '12345'
    }

@pytest.fixture()
def visacard():
    return {
        'cardno': '4242 4242 4242 4242',
        'cvv': '812',
        'expiry_month': '01',
        'expiry_year': '19',
        'pin': '3310',
        'otp': '12345'
    }

@pytest.fixture()
def visacard_local():
    return {
        'cardno': '4187427415564246',
        'cvv': '828',
        'expiry_month': '09',
        'expiry_year': '19',
        'pin': '3310',
        'otp': '12345'
    }

@pytest.fixture()
def visacard_intl():
    return {
        'cardno': '4556052704172643',
        'cvv': '899',
        'expiry_month': '01',
        'expiry_year': '19'
    }

@pytest.fixture()
def american_express_card_intl():
    return {
        'cardno': '344173993556638',
        'cvv': '828',
        'expiry_month': '01',
        'expiry_year': '18'
    }

@pytest.fixture()
def vervecard():
    return {
        'cardno': '5061020000000000094',
        'cvv': '347',
        'expiry_month': '07',
        'expiry_year': '20',
        'pin': '1111',
        'otp': '123456'
    }

@pytest.fixture()
def declined_card():
    return {
        'cardno': '5143010522339965',
        'cvv': '276',
        'expiry_month': '08',
        'expiry_year': '19',
        'pin': '3310'
    }

@pytest.fixture()
def fraudulent_card():
    return {
        'cardno': '5590131743294314',
        'cvv': '887',
        'expiry_month': '11',
        'expiry_year': '20',
        'pin': '3310',
        'otp': '12345'
    }

@pytest.fixture()
def insufficient_funds_card():
    return {
        'cardno': '5258585922666506',
        'cvv': '883',
        'expiry_month': '09',
        'expiry_year': '19',
        'pin': '3310',
        'otp': '12345'
    }

@pytest.fixture()
def preauth_card():
    return {
        'cardno': '5840406187553286',
        'cvv': '116',
        'expiry_month': '09',
        'expiry_year': '18',
        'pin': '1111',
    }

@pytest.fixture()
def required_envs():
    try:
        btn1_secret_key = os.environ['BTN1_SECRET_KEY']
        btn1_public_key = os.environ['BTN1_PUBLIC_KEY']
        btn1_auth_method = os.environ['BTN1_AUTH_METHOD']
        btn1_charge_type = os.environ['BTN1_CHARGE_TYPE']
    except KeyError as e:
        print('Please set required environment variable to run '\
            'integration tests')
        raise e

    return {
        'btn1_secret_key': btn1_secret_key,
        'btn1_public_key': btn1_public_key,
        'btn1_auth_method': btn1_auth_method,
        'btn1_charge_type': btn1_charge_type,
    }

@pytest.fixture()
def btn1_auth_details(required_envs):
    """
    Auth details that hold information about a button with a VBVSECURECODE
    auth model, a type of one-time, charge type of normal, and is not expired.
    """
    secret_key = required_envs['btn1_secret_key']
    public_key = required_envs['btn1_public_key']
    return AuthDetails(secret_key, public_key=public_key, env='DEV')

@pytest.fixture()
def direct_mastercard_charge_with_pin(btn1_auth_details,
    partial_charge_request1, mastercard):
    ravepy.set_auth(btn1_auth_details)
    req_kwargs = {}
    req_kwargs.update(partial_charge_request1)
    req_kwargs.update(mastercard)
    otp = req_kwargs.pop('otp')
    #pin = req_kwargs.pop('pin')
    return ravepy.Charge.create(source_type=CARD, **req_kwargs)

@pytest.fixture()
def direct_vervecard_charge_with_pin(btn1_auth_details,
    partial_charge_request1, vervecard):
    ravepy.set_auth(btn1_auth_details)
    req_kwargs = {}
    req_kwargs.update(partial_charge_request1)
    req_kwargs.update(vervecard)
    otp = req_kwargs.pop('otp')
    #pin = req_kwargs.pop('pin')
    return ravepy.Charge.create(source_type=CARD, **req_kwargs)

@pytest.fixture()
def direct_mastercard_charge_without_pin(btn1_auth_details,
    partial_charge_request1, mastercard):
    ravepy.set_auth(btn1_auth_details)
    req_kwargs = {}
    req_kwargs.update(partial_charge_request1)
    req_kwargs.update(mastercard)
    otp = req_kwargs.pop('otp')
    pin = req_kwargs.pop('pin')
    return ravepy.Charge.create(source_type=CARD, **req_kwargs)

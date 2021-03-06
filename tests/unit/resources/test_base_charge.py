from __future__ import absolute_import, unicode_literals

import pytest
from mock import MagicMock, patch,  PropertyMock, call

from ravepy.resources.charge import BaseCharge

def test_sorted_parameter_values(sample_request_data):
    with patch('ravepy.resources.charge.BaseCharge.charge_request_data',\
        new_callable=PropertyMock) as mocked_request_data:
        mocked_request_data.return_value = sample_request_data
        charge = BaseCharge(None)

        sorted_parameter_values = [
            'FLWPUBK-123456c59c8ef06749e6a72bc90e34a1-X', 'NG', 'USD'
        ]

        assert charge.sorted_parameter_values == sorted_parameter_values

def test_integrity_checksum(sample_auth_details, sample_request_data,
    sample_integrity_checksum):
    with patch('ravepy.resources.charge.BaseCharge.charge_request_data',\
        new_callable=PropertyMock) as mocked_request_data:
        mocked_request_data.return_value = sample_request_data
        charge = BaseCharge(sample_auth_details)

        assert charge.integrity_checksum == sample_integrity_checksum

def test__build_charge_request_data(sample_request_data, sample_original_request_data,\
    sample_auth_details):
    charge = BaseCharge(sample_auth_details)
    charge._original_charge_data = sample_original_request_data
    charge._build_charge_request_data()

    inv_map = {v:k for k, v in\
        list(BaseCharge.internal_to_external_field_map.items())}

    for key, value in charge.charge_request_data.items():
        # check that each key is a valid server api key
        assert key in list(BaseCharge.internal_to_external_field_map.values())
        assert value ==\
            charge._original_charge_data[inv_map[key]]

def test__send_request_no_poll(sample_auth_details):
    with patch('ravepy.resources.charge.BaseCharge.integrity_checksum',\
        new_callable=PropertyMock) as mocked_integrity_checksum:
        mocked_integrity_checksum.return_value = 'fakechecksum'

        with patch('ravepy.resources.charge.post') as post:
            charge = BaseCharge(sample_auth_details)
            data = {
                'PBFPubKey': sample_auth_details.public_key,
                'client': 'fakechecksum',
                'alg': '3DES-24'
            }
            charge._send_request_no_poll(
                sample_auth_details.urls.DIRECT_CHARGE_URL, data)

            post_call = call(sample_auth_details.urls.DIRECT_CHARGE_URL, data,
                headers=None)
            assert post.call_args == post_call

def test_sucessful_direct_charge_sets_charge_response_data(sample_auth_details):
    # TODO: test _direct_charge we are mocking it here without testing first
    with patch('ravepy.resources.charge.BaseCharge._direct_charge')\
        as mocked_direct_charge:
        req = {'ccv': '342'}
        resp = {
            'status': 'success',
            'data': {
                'flwRef': 'f34f3',
                'txRef': 'r343r'
            }
        }
        mocked_direct_charge.return_value = (req, resp)
        charge = BaseCharge(sample_auth_details)
        charge.charge()
        assert charge.charge_response_data == resp

def test_sucessful_direct_charge_sets_original_request_data(sample_auth_details):
    with patch('ravepy.resources.charge.BaseCharge._direct_charge')\
        as mocked_direct_charge:
        req = {'ccv': '342'}
        resp = {
            'status': 'success',
            'data': {
                'flwRef': 'f34f3',
                'txRef': 'r343r'
            }
        }
        mocked_direct_charge.return_value = (req, resp)
        charge = BaseCharge(sample_auth_details)
        charge.charge()
        assert charge._original_request_data == req

def test_sucessful_direct_charge_sets_raw_resp_data(sample_auth_details):
    with patch('ravepy.resources.charge.BaseCharge._direct_charge')\
        as mocked_direct_charge:
        req = {'ccv': '342'}
        resp = {
            'status': 'success',
            'data': {
                'flwRef': 'f34f3',
                'txRef': 'r343r'
            }
        }
        mocked_direct_charge.return_value = (req, resp)
        charge = BaseCharge(sample_auth_details)
        charge.charge()
        assert charge._raw_resp_data == resp

def test_sucessful_direct_charge_sets_transaction_refs(sample_auth_details):
    with patch('ravepy.resources.charge.BaseCharge._direct_charge')\
        as mocked_direct_charge:
        req = {'ccv': '342'}
        resp = {
            'status': 'success',
            'data': {
                'flwRef': 'f34f3',
                'txRef': 'r343r'
            }
        }
        mocked_direct_charge.return_value = (req, resp)
        charge = BaseCharge(sample_auth_details)
        charge.charge()
        assert charge._gateway_ref == resp['data']['flwRef']
        assert charge._merchant_ref == resp['data']['txRef']

def test_sucessful_validate_sets_validation_resp_data(sample_auth_details):
    with patch('ravepy.resources.charge.BaseCharge._send_request_no_poll')\
        as mocked_send_request_no_poll:
        req = {'ccv': '342'}
        resp = {
            'status': 'success',
            'data': {
                'flwRef': 'f34f3',
                'txRef': 'r343r'
            }
        }
        mocked_send_request_no_poll.return_value = resp
        charge = BaseCharge(sample_auth_details)
        with patch('ravepy.resources.charge.BaseCharge._get_validate_request_data')\
            as mocked_get_validate_request_data:
            mocked_get_validate_request_data.return_value = req
            charge.validate(1234)
            assert charge.validate_response_data == resp

def test_sucessful_validate_sets_original_request_data(sample_auth_details):
    with patch('ravepy.resources.charge.BaseCharge._send_request_no_poll')\
        as mocked_send_request_no_poll:
        req = {'ccv': '342'}
        resp = {
            'status': 'success',
            'data': {
                'flwRef': 'f34f3',
                'txRef': 'r343r'
            }
        }
        mocked_send_request_no_poll.return_value = resp
        charge = BaseCharge(sample_auth_details)
        charge.charge()
        with patch('ravepy.resources.charge.BaseCharge._get_validate_request_data')\
            as mocked_get_validate_request_data:
            mocked_get_validate_request_data.return_value = req
            charge.validate(1234)
            assert charge._original_request_data == req

def test_sucessful_validate_sets_raw_resp_data(sample_auth_details):
    with patch('ravepy.resources.charge.BaseCharge._send_request_no_poll')\
        as mocked_send_request_no_poll:
        req = {'ccv': '342'}
        resp = {
            'status': 'success',
            'data': {
                'flwRef': 'f34f3',
                'txRef': 'r343r'
            }
        }
        mocked_send_request_no_poll.return_value = resp
        charge = BaseCharge(sample_auth_details)
        charge.charge()
        with patch('ravepy.resources.charge.BaseCharge._get_validate_request_data')\
            as mocked_get_validate_request_data:
            mocked_get_validate_request_data.return_value = req
            charge.validate(1234)
            assert charge._raw_resp_data == resp

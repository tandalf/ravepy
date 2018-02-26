from __future__ import absolute_import, unicode_literals

import pytest
from mock import MagicMock, patch,  PropertyMock, call

from ravepy.resources.charge import BaseCharge

def test_sorted_parameter_values(sample_request_data):
    with patch('ravepy.resources.charge.BaseCharge.request_data',\
        new_callable=PropertyMock) as mocked_request_data:
        mocked_request_data.return_value = sample_request_data
        charge = BaseCharge(None)

        sorted_parameter_values = [
            'FLWPUBK-123456c59c8ef06749e6a72bc90e34a1-X', 'NG', 'USD'
        ]

        assert charge.sorted_parameter_values == sorted_parameter_values

def test_integrity_checksum(sample_auth_details, sample_request_data,
    sample_integrity_checksum):
    with patch('ravepy.resources.charge.BaseCharge.request_data',\
        new_callable=PropertyMock) as mocked_request_data:
        mocked_request_data.return_value = sample_request_data
        charge = BaseCharge(sample_auth_details)

        assert charge.integrity_checksum == sample_integrity_checksum

def test__build_request_data(sample_request_data, sample_original_request_data,\
    sample_auth_details):
    charge = BaseCharge(sample_auth_details)
    charge._original_request_data = sample_original_request_data
    charge._build_request_data()

    inv_map = {v:k for k, v in\
        list(BaseCharge.internal_to_external_field_map.items())}

    for key, value in charge.request_data.items():
        # check that each key is a valid server api key
        assert key in list(BaseCharge.internal_to_external_field_map.values())
        assert value ==\
            charge._original_request_data[inv_map[key]]

def test__send_charge_request(sample_auth_details):
    with patch('ravepy.resources.charge.BaseCharge.integrity_checksum',\
        new_callable=PropertyMock) as mocked_integrity_checksum:
        mocked_integrity_checksum.return_value = 'fakechecksum'

        with patch('ravepy.resources.charge.BaseCharge._send_post') as send_post:
            charge = BaseCharge(sample_auth_details)
            charge._send_charge_request()
            send_post_call = call({
                'PBFPubKey': sample_auth_details.public_key,
                'client': 'fakechecksum',
                'alg': '3DES-24'
            })
            assert charge._send_post.call_args == send_post_call

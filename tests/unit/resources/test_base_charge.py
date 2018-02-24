from __future__ import absolute_import, unicode_literals

import pytest
from mock import MagicMock, patch,  PropertyMock

from ravepy.resources.charge import BaseCharge

def test_sorted_parameter_values(sample_request_data):
    with patch('ravepy.resources.charge.BaseCharge.request_data',\
        new_callable=PropertyMock) as mocked_request_data:
        mocked_request_data.return_value = sample_request_data
        charge = BaseCharge(None)

        sorted_parameter_values = [
            'NG', 'USD', 'FLWPUBK-123456c59c8ef06749e6a72bc90e34a1-X'
        ]

        assert charge.sorted_parameter_values == sorted_parameter_values

def test_integrity_checksum(sample_auth_details, sample_request_data,
    sample_integrity_checksum):
    with patch('ravepy.resources.charge.BaseCharge.request_data',\
        new_callable=PropertyMock) as mocked_request_data:
        mocked_request_data.return_value = sample_request_data
        charge = BaseCharge(sample_auth_details)

        assert charge.integrity_checksum == sample_integrity_checksum

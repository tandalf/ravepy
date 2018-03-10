from __future__ import absolute_import, unicode_literals

import pytest

import ravepy
from ravepy.resources.auth import AuthDetails
from ravepy.resources.banks import Bank

def test_list_banks(btn1_auth_details):
    ravepy.set_auth(btn1_auth_details)
    banks = ravepy.Bank.list()

    assert len(banks) != 0
    for bank in banks:
        assert isinstance(bank, Bank)
        assert hasattr(bank, 'name')
        assert hasattr(bank, 'code')
        assert hasattr(bank, 'internet_banking')

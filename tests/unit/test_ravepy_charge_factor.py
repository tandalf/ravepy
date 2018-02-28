from __future__ import absolute_import, unicode_literals

import pytest

import ravepy
from ravepy.constants import CARD, ACCOUNT

def test_set_auth_details(sample_auth_details):
    ravepy.set_auth(sample_auth_details)
    ch = ravepy.Charge.create(source_type=CARD)
    assert ch._auth_details == sample_auth_details

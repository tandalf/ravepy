from __future__ import absolute_import, unicode_literals
from .base import RaveChargeError

__metaclass__ = type

class RavePinRequiredError(RaveChargeError):
    """
    Raise when a pin is required for a charge, but the pin was not provided.
    """
    pass

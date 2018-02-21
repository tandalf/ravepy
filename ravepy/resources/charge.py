from __future__ import absolute_import, unicode_literals

__metaclass__ = type

class BaseCharge:
    def __init__(self, *args, *kwargs):
        """
        The base class that all charge types inherit from. Concrete
        implementations of this would be a CardCharge and an AccountCharge.
        """
        pass

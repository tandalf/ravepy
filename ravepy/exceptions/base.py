from __future__ import absolute_import, unicode_literals

__metaclass__ = type

class RaveError(Exception):
    """
    Base exception for all ravepy specific exceptions.
    """
    pass

class RaveTimeoutError(RaveError):
    """
    Base exception for all timeout related exceptions that happen when making
    requests to rave. Most of the retry/polling flows will be enabled by this
    exception and it subclasses.
    """
    pass

class RaveChargeError(RaveError):
    """
    Base exception for problems that are more related to making a charge on
    rave. Except for timeouts in which case, a RaveTimeoutError would be
    more appropriate.
    """
    pass

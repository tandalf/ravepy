from __future__ import absolute_import, unicode_literals

__metaclass__ = type

class RaveError(Exception):
    """
    Base exception for all ravepy specific exceptions.
    """
    error_resp = None

class RaveGracefullTimeoutError(RaveError):
    """
    Base exception for all timeout related exceptions that happen when making
    requests to rave. Most of the retry/polling flows will be enabled by this
    exception and it subclasses. A ping_url should normally be provided in
    the exception. If not provided, a polling flow should automatically
    activated. I.e, methods like .charge, .validate, and .retrieve on a Charge
    instance should be recalled with the ping_url provided in the exception.
    the exception should also have a wait attribute which suggests the amount
    of seconds that the caller should sleep before retrying.
    """
    ping_url = None
    wait = 25
    status = None
    start_polling = False

class RaveChargeError(RaveError):
    """
    Base exception for problems that are more related to making a charge on
    rave. Except for timeouts in which case, a RaveTimeoutError would be
    more appropriate.
    """
    pass

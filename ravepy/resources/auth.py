from __future__ import absolute_import, unicode_literals

class AuthDetails:
    def __init__(self, secret_key, public_key=None):
        """
        AuthDetails provide a store for authentication parameters. This
        includes the secret and public key that was provided to you on your
        rave dashboard. It also provides a was for you to generate
        encryption keys that would be used for encrypting a Card or Account
        details.
        """
        self.secret_key = secret_key
        self.public_key = public_key
        self.encryption_key = None

    def encryptData(self, data):
        """
        Encrypts a card or account request that would be used to make a charge.
        """
        pass

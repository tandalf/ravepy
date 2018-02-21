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
        self._secret_key = secret_key
        self._public_key = public_key

    def getKey(self):
        """
        Gets an encryption key that will be used for encrypting card or
        account details before they are used in making a transaction.
        """
        pass

    def encryptData(self, data):
        """
        Encrypts a card or account request that would be used to make a charge.
        """
        pass

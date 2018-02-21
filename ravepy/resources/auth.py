from __future__ import absolute_import, unicode_literals

import base64
from Crypto.Cipher import DES3
import hashlib

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

        #implementation details from official web api docs
        hashedseckey = hashlib.md5(self.secret_key.encode("utf-8")).hexdigest()
        hashedseckeylast12 = hashedseckey[-12:]
        seckeyadjusted = self.secret_key.replace('FLWSECK-', '')
        seckeyadjustedfirst12 = seckeyadjusted[:12]
        self.encryption_key = seckeyadjustedfirst12 + hashedseckeylast12

    def encrypt_data(self, plain_text):
        """
        Encrypts a card or account request data that would be used to make a
        charge.
        """
        #implementation details from official web api docs
        md5Key = hashlib.md5(self.encryption_key.encode("utf-8")).digest()
        md5Key = md5Key + md5Key[0:8]

        blockSize = 8
        padDiff = blockSize - (len(plain_text) % blockSize)
        cipher = DES3.new(md5Key, DES3.MODE_ECB)

        plain_text = "{}{}".format(plain_text, "".join(chr(padDiff) * padDiff))
        return base64.b64encode(cipher.encrypt(plain_text))

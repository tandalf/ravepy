Auth Details
============
When you created a charge button on your dashboard, you were provided with certain credentials
like your a secret key, a public key and some other useful info that would be taken into
account when a payment is made with the button. These Details are encapsulated in
an AuthDetails class. An instance of this class would be used to encrypt, and provide
authentication details for the requests that would be made to rave. Example usage.

.. code-block:: python

   import os

   import ravepy
   from ravepy.resources.auth import AuthDetails

   #Get keys from environment variables of your choice
   secret_key = os.environ.get('RAVE_SECRET_KEY')
   public_key = os.environ.get('RAVE_PUBLIC_KEY')

   auth_details = AuthDetails(secret_key, public_key=public_key)

   # You can now set the authentication details that would be used to make requests
   # until it is change for some reason
   ravepy.set_auth(auth_details)

   # Create a charge and perform other actions of your choice
   ...

Staging/Development AuthDetails
+++++++++++++++++++++++++++++++
You might want to use the test endpoints as you develop you app. In this case, you
should create a staging/dev AuthDetails. By default, a live AuthDetails is created.

.. code-block:: python

  from rave import constants
  from ravepy.resources.auth import AuthDetails

  dev = constants.DEV
  auth_details = AuthDetails(secret_key, public_key=public_key, env=dev)

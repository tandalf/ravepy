Charging a Customer
===================
Rave provides mechanisms for placing different types of charge. You can charge user using
his debit/ATM card and through bank USSD codes. These are referred to as ``Card`` and ``Account``
charge respectively.

Creating a Card Charge
----------------------
When trying to create a card charge, a ``source_type`` of ``CARD`` should be provided as a
keyword param when calling the :py:meth:`ravepy.Charge.create`. For example, to create
a direct (not preauth) card charge, create the charge like this:

.. code-block:: python

    import ravepy
    from ravepy import constants
    from ravepy.resources.auth import AuthDetails

    auth_details = AuthDetails('My-secret-key', public_key='My-public-key')
    ravepy.set_auth(auth_details)

    ch = ravepy.Charge.create(source_type=constants.CARD, charge_type=constants.DIRECT_CHARGE,

        cardno='5438898014560229',
        cvv='789',
        expiry_month='09',
        expiry_year='19',
        pin='3310',
        otp='12345',

        ...

        )

The two special arguments here are the ``source_type`` which determines if the returned charge
would be a card or account charge. Also the ``charge_type`` which will determine if a charge would
use the preauth of normal flow see `Rave's API Docs <https://flutterwavedevelopers.readme.io/v2.0/reference>`_.

The other keyword arguments are documented here :ref:`create_kwargs`.

Creating a Preauth Charge
-------------------------
If you would be using the Preauth flow, then :py:meth:`ravepy.Charge.create` has to be
called like this

.. code-block:: python

    ch = ravepy.Charge.create(source_type=constants.CARD, charge_type=constants.PREAUTH_CHARGE,

        cardno='5438898014560229',
        cvv='789',
        expiry_month='09',
        expiry_year='19',
        pin='3310',
        otp='12345',

        ...

        )

.. _create_kwargs:

Valid Charge.create Keyword Arguments
-------------------------------------
Here are the keyword arguments that are valid when calling the :py:meth:`ravepy.Charge.create`
method. The dict below also shows a mapping of arguments to body params that will be encryted
before the charge is made. See `Rave Encryption Docs <https://flutterwavedevelopers.readme.io/v2.0/reference-edit/rave-encryption>`_

.. code-block:: python

    {
          'pub_key':                'PBFPubKey',
          'currency':               'currency',
          'country':                'country',
          'amount':                 'amount',
          'email':                  'email',
          'phone_number':           'phonenumber',
          'first_name':             'firstname',
          'last_name':              'lastname',
          'ip_address':             'IP',
          'merchant_ref':           'txRef',
          'device_fingerprint':     'device_fingerprint',

          #Card fields
          'cardno':                  'cardno',
          'cvv':                     'cvv',
          'expiry_month':            'expirymonth',
          'expiry_year':             'expiryyear',
          'pin':                     'pin',
          'suggested_auth':          'suggested_auth',
          'charge_type':             'charge_type',

          #Account fields
          'account_number':           'accountnumber',
          'account_bank':             'accountbank',
          'payment_type':             'payment_type',

          #Recurring billing fields include Card fields +
          'recurring_stop':           'recurring_stop',

          #USSD
          'payment_type':             'payment_type',
          'order_ref':                'orderRef',
          'is_ussd':                  'is_ussd',

          #Ghana Mobile Money
          'mobile_payment_type':      'payment-type',
          'network':                  'network',
          'is_mobile_money_gh':       'is_mobile_money_gh',

          #Mpesa
          'is_mpesa':                 'is_mpesa',

          #others
          'redirect_url':             'redirect_url',
      }

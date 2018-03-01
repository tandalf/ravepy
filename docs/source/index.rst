.. Rave documentation master file, created by
   sphinx-quickstart on Thu Mar  1 18:24:12 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Ravepy's documentation!
==================================
This documentation covers how to use the python client library for the rave payment
gateway. The library is very easy and straight forward to use.

.. warning::

   This library has not gotten to it's first alpha release. Bugs and uncompleted
   functions should be expects.

Getting Started
+++++++++++++++
To start using ravepy, install via pip

.. code-block:: sh

   pip install ravepy

If you want to install from source, you can clone the app from github and install
it's dependencies like this:

.. code-block:: sh

   git clone https://github.com/tandalf/ravepy.git
   cd ravepy
   pip install -r requirements.txt

If you would like to contribute to ravepy, please go ahead an install it's dev
dependencies.

.. code-block:: sh

   pip install -r requirements-dev.txt

The usage of ravepy is as easy as it's installation. For a sample of how to use
the library, see the code below. Note that for testing purposes, you need to
use one of the test cards provided on rave's website.

.. code-block:: python

   import ravepy
   from ravepy import constants
   from ravepy.resources.auth import AuthDetails

   auth_details = AuthDetails('My-secret-key', public_key='My-public-key')
   ravepy.set_auth(auth_details)
   
   ch = ravepy.Charge.create(source_type=constants.CARD,
          cardno='5438898014560229',
          cvv='789',
          expiry_month='09',
          expiry_year='19',
          pin='3310',
          otp='12345',
          currency=constants.NGN,
          country=constants.NIGERIA,
          amount='450',
          email='tim@live.com',
          phone_number='08081111111',
          first_name='Timothy',
          last_name='Ebiuwhe',
          ip_address='103.238.105.185',
          merchant_transaction_ref='MXX-ASC-4578')

    ch.charge() # calls the direct charge endpoint
    ch.validate() # calls the validation endpoint to place a direct charge

Placing a Direct Charge
-----------------------
After initiating a charge by calling the ``.charge`` method, your charge is put in
a pending state. You need to call ``.validate`` to commit the transaction like
it was done above.

Verifying a Transaction
-----------------------
When a charge has been made, it is advised that you verify the transaction before
giving value to your customer. Call the charge's ``.validate`` method to perform
sanity checks on your charge. This method calls rave's verification endpoints
to get the current transaction status, and then helps perform some sanity checks
on the returned response. Required arguments are the ``amount`` and ``currency``.
E.g,

.. code-block:: python

   ch.verify(450, constants.NGN)
   ch.verify(450, constants.NGN, status='success')
   ch.verify(450, constants.NGN, status='success', charge_code='00')


Inspecting Errors
-----------------
You can inspect the returned response from the server that cause ravepy to raise
an exception if one was raise, and the cause of the error was from the server. E.g,

.. code-block:: python

    try:
        ch.charge()
    except RaveChargeError as e:
        print("Could not not place charge")
        print(e.error_resp)

The response that cause the error to be raise would usually be available in the
exceptions ``.error_resp`` attribute.


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

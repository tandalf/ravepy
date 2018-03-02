
Welcome to Ravepy's documentation!
==================================
This documentation covers how to use the python client library for the rave payment
gateway. The library is very easy and straight forward to use.


Getting Started
===============
To start using ravepy, install via pip

```
  pip install ravepy
```

If you want to install from source, you can clone the app from github and install
it's dependencies like this:

```
git clone https://github.com/tandalf/ravepy.git
cd ravepy
pip install -r requirements.txt
```

If you would like to contribute to ravepy, please go ahead an install it's dev
dependencies.

```
pip install -r requirements-dev.txt
```

The usage of ravepy is as easy as it's installation. For a sample of how to use
the library, see the code below. Note that for testing purposes, you need to
use one of the test cards provided on rave's website.

```python
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
```

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

```python
ch.verify(450, constants.NGN)
ch.verify(450, constants.NGN, status='success')
ch.verify(450, constants.NGN, status='success', charge_code='00')
```

Inspecting Errors
-----------------
You can inspect the returned response from the server that cause ravepy to raise
an exception if one was raise, and the cause of the error was from the server. E.g,

```python
try:
    ch.charge()
except RaveChargeError as e:
    print("Could not not place charge")
    print(e.error_resp)
```

The response that cause the error to be raise would usually be available in the
exceptions ``.error_resp`` attribute.

Integrity Checksum
------------------
You can compute the integrity checksum of a direct charge request data by accessing Charge.integrity_checksum

```python
checksum = ch.integrity_checksum
```

Handling Transaction Timeouts
-----------------------------
Timeouts could occur at the service layer when making a request to rave. This is not the same as a connection timeout. A graceful timeout happens when internally at rave, some service or service provider takes too long to provide
a response. Rave gives you the ability to poll for the results of the transaction you were making when the timeout occurs. Here is an example of how to handle this in ravepy.

```python
try:
    ch.charge()
except RaveGracefullTimeoutError as e:
    if e.status == 'pending':
        reschedule_transaction.delay(ch.gateway_ref, e.ping_url)
```

The example above tries to make a charge, if a timeout occurs, behind the scenes it remakes the requests passing a url parameter `use_polling=1`. On making this request, a `ping_url` is returned which will be used to poll for the
response of the request you were making. If after remaking the request using polling and the transaction still times-out, it raises the `RaveGracefullTimeoutError` and sets the `.status` attribute of the exception instance to the status of the polling request. The `.ping_url` attribute of the exception instance is the `ping_url` that was provided by rave.
See [Rave's direct charge documentation](https://flutterwavedevelopers.readme.io/v2.0/reference#rave-direct-charge)

Using the ping_url
------------------
As stated above, when a request times-out, a `ping_url` is provided to enable the user poll for the transaction status. To use this ping url, you could
recall the charge method with the ping_url like so.

```python
ch.charge(ping_url=provided_ping_url)
```

Be aware that trying to poll doesn't guarantee that your request will be completed on your second trial. Another `RaveGracefullTimeoutError` could be
raise so you might need to wrap your code in another try/except block.

Also, you might need to perform the polling at a later time when the charge object that was used to make the initial request has been destroyed. For example, if you get a `RaveGracefullTimeoutError` and then schedule the charge to be polled later in another process (say, using celery). In this case, you would need to retrieve the charge instance, and then poll. The section below explains how to go about that.

Retrieving a Charge Instance (Requery and XRequery transaction status flow)
---------------------------------------------------------------------------
Lets say you need to know the status of a transaction later in the future after the charge has been initiated. Maybe to confirm the status of a charge at a later time. Ravepy provides a way for you to rebuild a charge instance if you have the gateway_ref (flwRef), or the merchant_transaction_ref (txRef). Example.

```python
    ch = ravepy.Charge.retrieve(gateway_ref='flwRef-fake', charge_type=constants.NORMAL_CHARGE)
    ch.verify(amount, currency)
```

The the charge_type keyword argument is either NORMAL_CHARGE or PRE_AUTH_CHARGE
to retrieve a card that was initiated using the normal auth model or the preauth model.

If instead for some reason, you wanted to used your own generated transaction ref that you used during initialization of the charge, you can pass in merchant_transaction_ref and set use_merchant_ref=True like so.

```python
    ch = ravepy.Charge.retrieve(use_merchant_ref=True, merchant_transaction_ref='my-fake-ref',
        charge_type=constants.NORMAL_CHARGE)
    ch.verify(amount, currency)
```

Documentation
-------------
There is a lot of implementation left to be documented, but it's quite easy to use.

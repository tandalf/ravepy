from __future__ import absolute_import, unicode_literals

__metaclass__ = type

class BaseCharge:
    required_fields = ['pub_key', 'first_name', 'last_name', 'ip_address',
        'merchant_transaction_ref']
    internal_to_external_field_map = [
        'pub_key': 'PBFPubKey',
        'currency': 'currency',
        'country': 'country',
        'amount': 'amount',
        'email': 'email',
        'phone_number': 'phonenumber',
        'first_name': 'firstname',
        'last_name': 'lastname',
        'ip_address': 'IP',
        'merchant_transaction_ref': 'txRef',
        'device_fingerprint': 'device_fingerprint',

        #Card fields
        'cardno': 'cardno',
        'ccv': 'ccv',
        'expiry_month': 'expirymonth',
        'expiry_year': 'expiryyear',
        'pin': 'pin',
        'suggested_auth': 'suggested_auth',
        'charge_type': 'charge_type',

        #Account fields
        'account_number': 'accountnumber',
        'account_bank': 'accountbank',
        'payment_type': 'payment_type',

        #Recurring billing fields include Card fields +
        'recurring_stop': 'recurring_stop',
    ]

    def __init__(self, auth_details, *args, *kwargs):
        """
        The base class that all charge types inherit from. Concrete
        implementations of this would be a CardCharge and an AccountCharge.
        This class would normally not be instantiated by the user
        """
        pass

    @property
    def data_dict(self):
        """
        Gets the JSON-like dict that will be the body of the payment request.
        """
        return self._data_dict

    @property
    def sorted_parameter_values(self):
        """
        Gets a sorted list of parameter values. The parameter values in this
        list has been sorted in a chronological order.
        """
        return []

    @property
    def integrity_checksum(self):
        """
        Gets the integrity checksum that would be sent to the client-side to
        help ensure the integrity of the user submitted data.
        """
        return ''

    def create(self, *args, **kwargs):
        """
        Create a new charge. On concrete subclasses, this might be a Card or
        an Account charge. When a charge is created like this, you can then
        call .charge() on it to initiate the charge.
        """
        raise NotImplemented('create is not implemented on the base class')

    def charge(self, *args, **kwargs):
        """
        Makes an API request to make the charge. This method encrypts the
        request data for you before sending the request to the server.
        """
        raise NotImplemented('Charge not implemented in base class')

from __future__ import absolute_import, unicode_literals

__metaclass__ = type

class BaseCharge:
    required_fields = ['pub_key', 'first_name', 'last_name', 'ip_address',
        'merchant_transaction_ref']
    internal_to_external_field_map = {
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
    }

    def __init__(self, auth_details, data=None, *args, **kwargs):
        """
        The base class that all charge types inherit from. Concrete
        implementations of this would be a CardCharge and an AccountCharge.
        This class would normally not be instantiated by the user
        """
        self._auth_details = auth_details
        self.was_retrieved = False
        self._req_data_dict = None
        self._res_data_dict = data
        self._sorted_parameter_values = None

    @property
    def request_data(self):
        """
        Gets the JSON-like dict that will be the body of the payment request.
        """
        return self._req_data_dict

    @property
    def response_data(self):
        """
        Gets the JSON-like dict that was the response to the most charge
        request.
        """
        return self._res_data_dict

    @property
    def sorted_parameter_values(self):
        """
        Gets a sorted list of parameter values. The parameter values in this
        list has been sorted in a chronological order. Parameter values are
        gotten from this.request_data.
        """
        if not self._sorted_parameter_values:
            self._sorted_parameter_values = []
            for key in sorted(self.request_data.keys()):
                self._sorted_parameter_values.append(self.request_data[key])

        return self._sorted_parameter_values

    @property
    def integrity_checksum(self):
        """
        Gets the integrity checksum that would be sent to the client-side to
        help ensure the integrity of the user submitted data. The
        integrity checksum is computed from the request_data property of the
        current charge.
        """
        plain_text = self._auth_details.secret_key + ''.join(self.sorted_parameter_values)
        return self._auth_details.encrypt_data(plain_text)

    @property
    def auth_url(self):
        """
        The auth_url that the client-side should redirect to incase of a
        3DSecure auth model.
        """
        pass

    def create(self, *args, **kwargs):
        """
        Create a new charge. On concrete subclasses, this might be a Card or
        an Account charge. When a charge is created like this, you can then
        call .charge() on it to initiate the charge.
        """
        raise NotImplemented('create is not implemented on the base class')

    def _build_request_data(self):
        pass

    def _can_use_pin_auth_model(self):
        pass

    def _can_use_3dsecure_auth_model(self):
        pass

    def _needs_pin_auth(self, response_dict):
        pass

    def charge(self, redirect_url=None, ping_url=None, *args, **kwargs):
        """
        Makes an API request to make the charge. This method encrypts the
        request data for you before sending the request to the server.
        """
        #Encrypt card details see
        #https://flutterwavedevelopers.readme.io/v1.0/reference#rave-encryption
        #-2

        #build and send request

        #Check for case where card is local mastercard or verve and resend

        #Remember to set auth_url in case you need to

        raise NotImplemented('Charge not implemented in base class')

    def _send_charge_request(self, auth_model):
        pass

    def validate_charge_response(self):
        raise NotImplemented("Validation of charge no implemented")

    @classmethod
    def retrieve(cls, auth_details, gateway_ref=None, merchant_ref=None,
        ping_url=None):
        """
        Retrieves a charge resource from the API gateway. This class method
        creates an instance of this class and tries it's best to reconstruct
        what the initial request and response must have looked like when the
        charge was first made.

        Args:
            auth_details: The AuthDetails that will be used to make an
                authenticated request to retrieve the card.
        Kwargs:
            gateway_ref: (optional) The transaction reference the gateway
                returned when the charge was initiated. If this is provided the
                normal requery transaction verification flow is used to
                retrieve the charge. If not provided, the merchant_ref is
                required.
            merchant_ref: (optional) The merchant transaction unique reference
                that was provided by the user when the charge was first
                initiated. If param is provided, then the xrequery flow is used
                to retrieve the charge. If not provided, then gateway_ref is
                required.
            ping_url: (optional) A url that would be used to implement the
                flow for retrieving a charge status. The presence of this
                param indicates that we have tried to retrieve the charge
                status before, but the request timed out, and we are now
                polling to get the charge data.
        Note:
            when a charge is retrieved, certain actions like calling
            charge again should fail.
        """
        pass

    def sanity_checks(self, amount, currency, status='success', charge_code=0,
        *args, **kwargs):
        """
        Performs basic sanity checks on the charge. The charge should have
        been initiated on the gateway before calling this method. More
        concretely, it should have a transaction reference assigned to it at
        the point where this method will be called.
        """
        pass

    @classmethod
    def banks(cls, country):
        """
        Retrieves the list of Banks for a given country.
        """
        pass

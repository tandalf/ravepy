from __future__ import absolute_import, unicode_literals

from ravepy.exceptions.base import RaveError
from ravepy.exceptions.charge import RavePinRequiredError, RaveChargeError

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

        #others
        'redirect_url': 'redirect_url',
    }

    def __init__(self, auth_details, data=None, *args, **kwargs):
        """
        The base class that all charge types inherit from. Concrete
        implementations of this would be a CardCharge and an AccountCharge.
        This class would normally not be instantiated by the user
        """
        self._auth_details = auth_details
        self.was_retrieved = False
        self._original_request_data = None
        self._req_data_dict = None
        self._charge_res_data_dict = None
        self._validation_resp_data_dict = None
        self._sorted_parameter_values = None

        self._charge_type = None
        self._gateway_ref = None
        self._merchant_ref = None

    @property
    def request_data(self):
        """
        Gets the JSON-like dict that will be the body of the payment request.
        """
        return self._req_data_dict

    @property
    def charge_response_data(self):
        """
        Gets the JSON-like dict that was the response to the most charge
        request.
        """
        return self._charge_res_data_dict

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
        self._original_request_data = kwargs
        self._build_request_data()

    def _build_request_data(self):
        # Convert original request data that was gotten from the kwargs of a
        # method, and converts them into a payload that the server expects
        #
        self._req_data_dict = {}
        for key, value in self._original_request_data.items():
            if key not in BaseCharge.internal_to_external_field_map.keys():
                raise RaveError(
                    'Unkown key \'{}\' while trying to build request'.format(
                        key))
            self._req_data_dict[BaseCharge.internal_to_external_field_map[key]]\
                = value

        return self._req_data_dict

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
        A card that was reconstructed by either calling retrieve or consume
        cannot be charged a second time. More concretely, if was_retrieved
        is set to True, this method will raise a RaveChargeError.
        """
        #Encrypt card details see
        #https://flutterwavedevelopers.readme.io/v1.0/reference#rave-encryption
        #-2

        #build and send request

        #Check for case where card is local mastercard or verve and resend

        #Remember to set auth_url in case you need to

        raise NotImplemented('Charge not implemented in base class')

    def _send_charge_request(self):
        direct_charge_body = {
            'PBFPubKey': self._auth_details.public_key,
            'client': self.integrity_checksum,
            'alg': '3DES-24'
        }
        return self._send_post(direct_charge_body)

    def _send_post(self, body):
        pass

    def validate(self, otp):
        """
        After a direct charge is made, the transaction will be in a pending
        state. Calling this method makes the actual charge. Calling this
        method for the preauth flow raises a RaveChargeError.

        Args:
            otp: the one time password that was sent to the paying user
        """
        raise NotImplemented("Validation of charge not implemented")

    def capture(self):
        """
        Captures a charge that was created using the preauth transaction
        flow. Calling this method for the normal(non preauth) raises a
        RaveChargeError
        """
        raise NotImplemented("Capture is not implemented in base class")

    @classmethod
    def retrieve(cls, auth_details, charge_type, gateway_ref=None,
        merchant_ref=None, ping_url=None):
        """
        Retrieves a charge resource from the API gateway. This class method
        creates an instance of this class that would be used for verification
        purposes or for the sake of capturing in case the preauth was used
        for initiating the charge. The charge method is not meant to be called
        again on a retrieved instance. Sets was_retrieved to true on the
        new instance.

        Args:
            auth_details: The AuthDetails that will be used to make an
                authenticated request to retrieve the card. And would also be
                used to instantiate the new Charge.
            charge_type: The charge_type that was used to initialize the
                charge the first time, can be either PRE_AUTH_CHARGE or
                NORMAL_CHARGE.
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

    @classmethod
    def retrieve_from_webhook(self, auth_details, data):
        """
        This is used when the VBVSECURECODE or the AVS_VBVSECURECODE auth
        models were used in making a direct charge. Like the retrieve method,
        this method is used to collect the response to a validate request,
        but unlike the retrieve method, this does not make a call to the server
        instead, it is used to consume the validation response that was sent
        to your redirect_url body parameter when the direct charge call was
        made. Sets was_retrieved to true on the new instance.

        Args:
            auth_details: The authentication detail that will be used to
                instantiate the new Charge instance.
            data: The data that has been collected by your server and
                transformed into a dict.

        Returns:
            BaseCharge: a Charge of the appropriate type that holds information
            about the charge that was consumed.
        """
        pass

    def verify(self, amount, currency, status='success', charge_code=0,
        *args, **kwargs):
        """
        Performs basic sanity checks on the charge. The charge should have
        been initiated on the payment gateway before calling this method. More
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

class CardCharge(BaseCharge):
    def charge(self, ping_url=None, pin=None, *args, **kwargs):
        """
        Makes a charge request with to the api server. If this charge instance
        was rebuilt by retreiving it from the server, i.e, it was not built
        from scratch by calling create, a RaveChargeError will be raised.
        """
        if self.was_retrieved:
            raise RaveChargeError(
                'Cannot charge a card that was reconstructed. Use create.')

        if not ping_url:
            resp_data = self._send_charge_request()
            if resp_data['SUGGESTED_AUTH'] == 'PIN' and not pin:
                raise RaveError('Pin required for this transaction')

            self._original_request_data.update({'SUGGESTED_AUTH': 'PIN',
                'pin': pin})
            self._build_request_data()
            resp_data = self._send_charge_request()

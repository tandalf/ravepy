from __future__ import absolute_import, unicode_literals
import json

from ravepy.utils.http import post
from ravepy.exceptions.base import RaveError, RaveGracefullTimeoutError
from ravepy.exceptions.charge import (
    RavePinRequiredError, RaveChargeError
)
from ravepy.constants import NORMAL_CHARGE, PRE_AUTH_CHARGE, CARD, ACCOUNT

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
        'cvv': 'cvv',
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

        #USSD
        'payment_type': 'payment_type',
        'order_ref': 'orderRef',
        'is_ussd': 'is_ussd',

        #Ghana Mobile Money
        'mobile_payment_type': 'payment-type',
        'network': 'network',
        'is_mobile_money_gh': 'is_mobile_money_gh',

        #Mpesa
        'is_mpesa': 'is_mpesa',

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
        self._charge_req_data_dict = None
        self._charge_res_data_dict = None
        self._validation_resp_data_dict = None
        self._verification_resp_data_dict = None
        self._preauth_resp_data = None
        self._transaction_status_resp_data = None
        self._raw_resp_data = None
        self._sorted_parameter_values = None

        self._charge_type = None
        self._gateway_ref = None
        self._merchant_ref = None

        self._is_preauth = False

    @property
    def charge_request_data(self):
        """
        Gets the JSON-like dict that will be the body of the payment request.
        """
        return self._charge_req_data_dict

    @property
    def charge_response_data(self):
        """
        Gets the JSON-like dict that was the response to a direct charge
        request.
        """
        return self._charge_res_data_dict

    @property
    def validate_response_data(self):
        """
        Gets the JSON-like dict that was the response to a validate request
        for the charge.
        """
        return self._validation_resp_data_dict

    @property
    def verification_response_data(self):
        """
        Gets the JSON-like dict that was the response to a validate request
        for the charge.
        """
        return self._verification_resp_data_dict

    @property
    def preauth_response_data(self):
        """
        Gets the JSON-like dict that was the response to a preath card charge
        request.
        """
        return self._preauth_resp_data

    @property
    def transaction_status_response_data(self):
        """
        Gets the JSON-like dict that was the most recent response to a
        transaction status request.
        """
        return self._transaction_status_resp_data

    @property
    def raw_response_data(self):
        """
        Gets the JSON-like dict that was the response to the most recent
        request that was made on this instance. Unlike the other response data
        attributes, this one has not be cleaned or modified in any way.
        """
        return self._raw_resp_data

    @property
    def sorted_parameter_values(self):
        """
        Gets a sorted list of parameter values. The parameter values in this
        list has been sorted in a chronological order. Parameter values are
        gotten from this.request_data.
        """
        if not self._sorted_parameter_values:
            self._sorted_parameter_values = []
            for key in sorted(self.charge_request_data.keys()):
                self._sorted_parameter_values.append(self.charge_request_data[key])

        return self._sorted_parameter_values

    @property
    def integrity_checksum(self):
        """
        Gets the integrity checksum that would be sent to the client-side to
        help ensure the integrity of the user submitted data. The
        integrity checksum is computed from the request_data property of the
        current charge.
        """
        plain_text = self._auth_details.secret_key + ''.join(
            self.sorted_parameter_values)
        return self._auth_details.encrypt_data(plain_text)

    @property
    def auth_url(self):
        """
        The auth_url that the client-side should redirect to incase of a
        3DSecure auth model.
        """
        pass

    def create(self, charge_type=NORMAL_CHARGE, *args, **kwargs):
        """
        Create a new charge. On concrete subclasses, this might be a Card or
        an Account charge. When a charge is created like this, you can then
        call .charge() on it to initiate the charge.
        """
        self._charge_type = charge_type
        self._original_request_data = kwargs
        self._original_request_data['pub_key'] = self._auth_details.public_key
        if kwargs.get('pin'):
            self._original_request_data.update({'suggested_auth': 'PIN'})
        self._build_charge_request_data()

    def _build_charge_request_data(self):
        # Convert original request data that was gotten from the kwargs of a
        # method, and converts them into a payload that the server expects
        #
        self._charge_req_data_dict = {}
        for key, value in self._original_request_data.items():
            if key not in BaseCharge.internal_to_external_field_map.keys():
                raise RaveError(
                    'Unkown key \'{}\' while trying to build request'.format(
                        key))
            self._charge_req_data_dict[BaseCharge.internal_to_external_field_map[key]]\
                = value

        return self._charge_req_data_dict

    def _can_use_pin_auth_model(self):
        pass

    def _can_use_3dsecure_auth_model(self):
        pass

    def _needs_pin_auth(self, response_dict):
        pass

    def charge(self, redirect_url=None, ping_url=None, pin=None, *args, **kwargs):
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

        if self.was_retrieved:
            raise RaveChargeError(
                'Cannot charge a card that was reconstructed. Use create.')
        req_data = self._get_direct_charge_request_data()

        if not ping_url:
            try:
                resp_data = self._send_request_no_poll(
                    self._auth_details.urls.DIRECT_CHARGE_URL ,req_data)
                if resp_data['data'].get('suggested_auth') == 'PIN':
                    pin = pin if pin else req_data.get('pin')
                    if not pin:
                        raise RaveChargeError('Pin required for this transaction')
                    else:
                        self._original_request_data.update({'suggested_auth': 'PIN',
                            'pin': pin})
                        self._build_charge_request_data()
                        req_data = self._get_direct_charge_request_data()
                        resp_data = self._send_request_no_poll(
                            self._auth_details.urls.DIRECT_CHARGE_URL, req_data)

            except RaveGracefullTimeoutError as e:
                ping_url = e.ping_url if e.ping_url else ping_url
                if e.start_polling:
                    resp_data = self._send_request_no_poll(
                        self._auth_details.urls.DIRECT_CHARGE_URL, req_data,
                        switcht_to_polling=True)
                else:
                    raise e

        else:
            resp_data = self._send_request_by_polling(ping_url)

        if resp_data['status'] != 'success':
            e = RaveChargeError('Charge request failed. See e.error_resp')
            e.error_resp = resp_data
            raise e

        self._original_request_data = req_data
        self._charge_res_data_dict = resp_data
        self._raw_resp_data = resp_data
        self._gateway_ref = resp_data['data']['flwRef']
        self._merchant_ref = resp_data['data']['txRef']

        return resp_data

    def _get_direct_charge_request_data(self):
        client = self._auth_details.encrypt_data(json.dumps(
            self._charge_req_data_dict))
        return {
            'PBFPubKey': self._auth_details.public_key,
            'client': client,
            'alg': '3DES-24'
        }

    def _send_request_no_poll(self, url, req_data, switch_to_polling=False):
        if switch_to_polling:
            resp_data = post(url + '?use_polling=1', req_data)
            if resp_data['status'] == 'success':
                ping_url = resp_data['data']['ping_url']
                e = RaveGracefullTimeoutError("Poll for response on url {}"\
                    .format(ping_url))
                e.ping_url = ping_url
            else:
                raise RaveChargeError('Could not switch to polling')
        else:
            resp_data = post(url, req_data)
            if resp_data['status'] == 'error' and\
                resp_data['data'].get('status') == 'failed':
                e = RaveGracefullTimeoutError(
                    "Timeout while sending charge request. Please switch to"\
                    " polling.")
                e.start_polling = True
                raise e

        return resp_data

    def _send_request_by_polling(self, ping_url):
        resp_data = get(ping_url)
        ping_url = resp_data['data'].get('ping_url')
        success_data = resp_data['data'].get('response')
        data_status = resp_data['data'].get('status')

        if data_status == 'completed':
            return json.loads(success_data)
        if data_status == 'pending':
            e = RaveGracefullTimeoutError('Transaction pending')
            e.status = 'pending'
        else:
            e = RaveGracefullTimeoutError('Transaction failed. Status: {}'\
                .format(data_status))
            e.status = data_status

    def validate(self, otp, ping_url=None):
        """
        After a direct charge is made, the transaction will be in a pending
        state. Calling this method makes the actual charge. Calling this
        method for the preauth flow raises a RaveChargeError.

        Args:
            otp: the one time password that was sent to the paying user

        Kwargs:
            ping_url: If present, this is the url that will be used for polling
                the validate request if a timeout response was initially
                received.

        Raises:
            RaveGracefullTimeoutError: if a timeout response is sent from
                the server. Read the docs for RaveGracefullTimeoutError for
                info on how to handle this exception gracefully.
        """
        if self._charge_type==PRE_AUTH_CHARGE or self._preauth_resp_data:
            raise RaveChargeError('Cannot call the calidate response for '\
                'a preauth flow. Call capture instead')

        if ping_url:
            resp_data = self._send_request_by_polling(ping_url)
        else:
            req_data = self._get_validate_request_data(otp)
            resp_data = self._send_request_no_poll(
                self._auth_details.urls.VALIDATE_CARD_CHARGE_URL, req_data)

        self._original_request_data = req_data
        self._validation_resp_data_dict = resp_data
        self._raw_resp_data = resp_data

    def _send_validate_request(self, otp):
        validate_request_body = {
            'PBFPubKey': self._auth_details.public_key,
            'transaction_reference': self._gateway_ref,
            'otp': otp,
        }
        resp = self._send_post(validate_request_body)

        # Check if a polling is required and raise a valid exception

    def _send_validate_request_by_polling(self, otp, ping_url):
        #if no ping_url in data, return response else reraise error
        pass

    def capture(self):
        """
        Captures a charge that was created using the preauth transaction
        flow. Calling this method for the normal(non preauth) raises a
        RaveChargeError
        """
        raise NotImplemented("Capture is not implemented in base class")

    @classmethod
    def retrieve(cls, auth_details, charge_type=None, gateway_ref=None,
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
        Kwargs:
            charge_type: The charge_type that was used to initialize the
                charge the first time, can be either PRE_AUTH_CHARGE or
                NORMAL_CHARGE.
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
        the point where this method will be called. Either the
        self.validate_response_data or self.preauth_response_data should be
        available by the time this method is called.
        """
        pass

    @classmethod
    def banks(cls, country):
        """
        Retrieves the list of Banks for a given country.
        """
        pass

class CardCharge(BaseCharge):
    def _get_validate_request_data(self, otp):
        return {
            'PBFPubKey': self._auth_details.public_key,
            'transaction_reference': self._gateway_ref,
            'otp': otp
        }

    @classmethod
    def retrieve(cls, auth_details, charge_type=None, gateway_ref=None,
        merchant_ref=None, use_merchant_ref=False, ping_url=None):
        if not charge_type:
            raise RaveChargeError('Charge type should be specified. Options '\
                'are {} or {}.'.format(NORMAL_CHARGE, PRE_AUTH_CHARGE))
        if charge_type != PRE_AUTH_CHARGE and\
            ((gateway_ref or merchant_ref) == False):
            raise RaveChargeError('The gateway_ref (flwRef), or the '\
                'merchant_ref you used must be provided except when using '\
                'preauth flow')

        if ping_url:
            # TODO: work on polling case
            pass
        else:
            charge = CardCharge(auth_details)
            req_data = {
                'SECKEY': auth_details.secret_key
            }
            if use_merchant_ref:
                req_data.update({
                    'txref': merchant_ref,
                    'last_attempt': 1,
                    'only_successful': 1})
                resp_data = charge._send_request_no_poll(
                    auth_details.urls.TRANSACTION_VERIFICATION_XREQUERY_URL,
                    req_data)
            else:
                resp_data = req_data.update({
                    'flw_ref': gateway_ref,
                    'normalize': 1
                })
                resp_data = charge._send_request_no_poll(
                    auth_details.urls.TRANSACTION_VERIFICATION_URL, req_data)

        charge._gateway_ref = gateway_ref
        charge._merchant_ref = merchant_ref
        charge._raw_resp_data = resp_data
        charge._verification_resp_data_dict = resp_data
        charge.was_retrieved = True
        return charge

    def retrieve_from_webhook(cls, auth_details, data):
        charge = CardCharge(auth_details, data=data)
        charge._gateway_ref = resp_data['data']['flwRef']
        charge._merchant_ref = resp_data['data']['txRef']
        charge._raw_resp_data = resp_data
        charge.was_retrieved = True
        return charge


class AccountCharge(BaseCharge):
    def _get_validate_request_data(self, otp):
        return {
            'PBFPubKey': self._auth_details.public_key,
            'transactionreference': self._gateway_ref,
            'otp': otp
        }

class ChargeFactory:
    def __init__(self, data=None, *args, **kwargs):
        self._data = data
        self._args = args
        self._kwargs = kwargs
        self._charge = None
        self._source_type = None

    def create(self, source_type=CARD, *args, **kwargs):
        self._source_type = source_type
        if source_type == CARD:
            charge = CardCharge(self._auth_details, *self._args,
                **self._kwargs)
        elif source_type == ACCOUNT:
            charge = AccountCharge(self._auth_details, *self._args,
                **self._kwargs)
        else:
            raise RaveChargeError('Invalid source type. Must be {} or {} not {}'\
                .format(CARD, ACCOUNT, source_type))

        charge.create(*args, **kwargs)
        return charge

    def retrieve(self, auth_details, charge_type=None, gateway_ref=None,
        merchant_ref=None, use_merchant_ref=False, ping_url=None,
        source_type=None):
        """
        Performs the same actions as it's base class but automatically creates
        the right type of charge instance based on the source_type param.
        Kwargs:
            source_type: The type of charge to instantiate. Default is CARD.
        """
        print('source_type')
        print(source_type)
        if source_type == CARD:
            charge = CardCharge.retrieve(auth_details, charge_type,
                gateway_ref, merchant_ref, use_merchant_ref, ping_url)
        elif source_type == ACCOUNT:
            charge = AccountCharge.retrieve(auth_details, charge_type,
                gateway_ref, merchant_ref, use_merchant_ref, ping_url)
        else:
            raise RaveChargeError('Invalid source type. Must be {} or {} not {}'\
                .format(CARD, ACCOUNT, source_type))

        return charge

        def retrieve_from_webhook(self, source_type=CARD, *args, **kwargs):
            """
            Performs the same actions as it's base class but automatically creates
            the right type of charge instance based on the source_type param.
            Kwargs:
                source_type: The type of charge to instantiate. Default is CARD.
            """
            if source_type == CARD:
                charge = CardCharge.retrieve_from_webhook(*args,
                    **kwargs)
            elif source_type == ACCOUNT:
                charge = AccountCharge.retrieve_from_webhook(*args,
                    **kwargs)
            else:
                raise RaveChargeError('Invalid source type. Must be {} or {}'\
                    .format(CARD, ACCOUNT))

            return charge

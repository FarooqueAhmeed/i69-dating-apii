import jwt
import requests
import json
import hashlib

from datetime import datetime, timedelta

from .models import PrivateKey


class Boku(object):
    """
    Management of all Boku code goes from this class
    """

    def __init__(self):
        pass

    def generate_payment_token(self, private_key, body_sha256=None):
        """
        Method to generate a JWT RS256 token for the payment authorization in BOKU.
        Returns: EncodedToken
        """
        headers = {"alg": "RS256", "typ": "JWT"}

        now = datetime.now()
        two_days_later = now + timedelta(days=2)

        payload = {
            "exp": str(int(round(two_days_later.timestamp()))),
            "nbf": str(int(round(now.timestamp()))),
            "iat": str(int(round(now.timestamp()))),
        }

        if body_sha256:
            payload["body_sha256"] = body_sha256

        """CHECK THE BODY from the checksum response"""

        return jwt.encode(payload, private_key, algorithm="RS256", headers=headers)

    def decode_payment_request(self, request):
        """
        This function would decode the token received in the response from BoKu
        dashboard. It would also verify the key_signature of the request.
        We can further use body_sha256 from the payload to verify the request
        with funtion is_valid_body.
        """

        token = request.headers["X-Fortumo-Content-Signature"]

        # TODO: Need to add the private key and public key text in the variables below.
        public_key = (
            public_key.objects.filter(payment_gateway="boku").last().key_text.encode()
        )

        return jwt.decode(token, public_key, algorithms=["RS256"])

    def is_valid_body(self, body_sha256, decoded_token):
        """
        Validate the sha256 responses recived.
        """
        received_sha256 = decoded_token["body_sha256"]

        if body_sha256 == received_sha256:
            return True

        return False

    def make_get_request(self, url):
        """
        Method to make a get request using the boku credentials.
        """

        # TODO: Get Private Key from the Database
        if not PrivateKey.objects.filter(payment_gateway="boku").exists():
            print("Private Key not found for Boku")
            return {"error": True}
        private_key = (
            PrivateKey.objects.filter(payment_gateway="boku").last().key_text.encode()
        )

        # GENERATE TOKEN
        token = self.generate_payment_token(private_key=private_key)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
        else:
            data = {"error": True}

        return data

    def generate_body_sha256(self, body):
        """
        Function to hash the body dictionary to sha256.
        Returns SHA256 hash for the dictionary object.
        """
        encoded_body = json.dumps(body, sort_keys=True).encode()
        body_sha256 = hashlib.sha256(encoded_body).hexdigest()

        return body_sha256

    def make_post_request(self, url, body):
        """
        Test function to make a post request.
        """

        # TODO: Get Private Key from the Database
        if not PrivateKey.objects.filter(payment_gateway="boku").exists():
            print("Private Key not found for Boku")
            return False
        private_key = (
            PrivateKey.objects.filter(payment_gateway="boku").last().key_text.encode()
        )

        body_sha256 = self.generate_body_sha256(body)

        # GENERATE TOKEN
        token = self.generate_payment_token(
            private_key=private_key, body_sha256=body_sha256
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        }

        response = requests.post(
            url, headers=headers, data=json.dumps(body, sort_keys=True)
        ).json()

        if response["code"] == 200:
            return True
        else:
            return False

    def make_put_request(self, url, body):
        """
        Test function to make a post request.
        """

        if not PrivateKey.objects.filter(payment_gateway="boku").exists():
            print("Private Key not found for Boku")
            return False

        private_key = (
            PrivateKey.objects.filter(payment_gateway="boku").last().key_text.encode()
        )

        body_sha256 = self.generate_body_sha256(body)

        # GENERATE TOKEN
        token = self.generate_payment_token(
            private_key=private_key, body_sha256=body_sha256
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        }

        response = requests.put(
            url, headers=headers, data=json.dumps(body, sort_keys=True)
        ).json()

        if response["code"] == 200:
            return True
        else:
            return False

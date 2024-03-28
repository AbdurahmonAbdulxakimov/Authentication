from twilio.rest import Client
from django.conf import settings

import random


def generate_verification_code():
    return random.randint(100000, 999999)


def send_sms_verification(phone_number, verification_code):
    # Use Twilio to send SMS with verification code
    print("\n", settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN, "\n")
    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    # message = client.messages.create(
    #     body=f"Your verification code is: {verification_code}",
    #     from_=settings.TWILIO_PHONE_NUMBER,
    #     to=phone_number,
    # )
    verification_check = client.verify.v2.services(
        "VAdb007d2857a9bd8c1fdd2900c49f1981"
    ).verifications.create(
        to=phone_number,
        channel="sms",
        custom_message=f"Your verification code is: {verification_code}",
    )

    print(f"Verification code sent to {phone_number}: {verification_code}")

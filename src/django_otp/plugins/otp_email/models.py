from django.core.mail import send_mail
from django.template.loader import render_to_string

from django_otp.models import SideChannelDevice
from django_otp.util import hex_validator, random_hex

from .conf import settings


def default_key():
    return random_hex(20)


def key_validator(value):
    return hex_validator()(value)


class EmailDevice(SideChannelDevice):
    """
    A :class:`~django_otp.models.SideChannelDevice` that delivers a token to the user's
    registered email address (``user.email``). This is intended for
    demonstration purposes; if you allow users to reset their passwords via
    email, then this provides no security benefits.
    """

    def generate_challenge(self):
        self.generate_token(valid_secs=settings.OTP_EMAIL_TOKEN_VALID_SECS)
        body = render_to_string('otp/email/token.txt', {'token': self.token})

        send_mail(settings.OTP_EMAIL_SUBJECT,
                  body,
                  settings.OTP_EMAIL_SENDER,
                  [self.user.email])

        message = "sent by email"

        return message

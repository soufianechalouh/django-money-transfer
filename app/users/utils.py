from django.conf import settings
from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(data["email_subject"], data["email_body"],
                             from_email=settings.EMAIL_HOST_USER, to=[data["to"]])
        email.send()

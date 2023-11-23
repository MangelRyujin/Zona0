from dj_rest_auth.serializers import PasswordResetSerializer
from django.conf import settings
from utils.send_email.send_email import format_frontend_url


class CustomPasswordResetSerializer(PasswordResetSerializer):
    
    def get_email_options(self):
        path = "/accounts/password-reset/confirm/"
        frontend_url = format_frontend_url(path)
        return {
            'subject_template_name': 'account/email/password_reset_key_subject.txt',
            'extra_email_context': {"link": frontend_url},
       }

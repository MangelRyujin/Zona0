from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from utils.send_email.send_email import unsign_value

@api_view(["GET"])
def email_verification(request, token):
    """
    Email verification view.

    Tokens are only valid for 24 hours.
    """
    if not (value := unsign_value(token, max_age=60 * 60 * 24)):
        
        return Response(
            {
                "non_field_errors": [_("Invalid verification token.")],
            },
            status=400,
        )

    user = get_object_or_404(get_user_model(), pk=int(value))

    if not user.verified_email:
        user.verify_email()
    return Response({"message": _("Email verified.")}, status=200)

from django.core.mail import send_mail
from django.conf import settings
from django.core.signing import TimestampSigner,BadSignature, SignatureExpired
from contextlib import suppress

signer = TimestampSigner()

def format_frontend_url(path):
    front_url = settings.FRONTEND_URL
    return f"{front_url}{path}"



def sign_value(value):
    """
    Signs a value with the secret key. Useful to create verification tokens
    """
    return signer.sign(value)


def unsign_value(signed, max_age=None):
    """
    Unsigns a value and returns it
    """
    value = None
    with suppress(BadSignature, SignatureExpired):
        value = signer.unsign(signed, max_age=max_age)
    return value



def send_email_create_manager_incorrect(user, email):
    send_mail(
    'Alguien ha intentado burlar la seguridad',
    f'El usuario {user} con el correo {email} ha intentado registrar un usuario manager sin permiso, se ha vaneado por seguridad',
    settings.EMAIL_HOST_USER,
    ['bullsabdbears@gmail.com'],
    fail_silently=False
)
   
   
def send_email_verify(email , enlace, token):
    send_mail(
    f'Bienvenido {email} a Zona 0',
    f'Para verificar su registro puede copiar el codigo a continuación: {token} \n Si desea acceder a nuestra web verifique su registro por el siguiente elnace: {settings.FRONTEND_URL}{enlace}',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False
)
   

def send_email_transfer(user,email,valor):
    send_mail(
    f'Transferencia realizada en Zona 0',
    f'Usted ha resivido una transferencia de {valor} ZOP efectuada por el usuario {user}',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False
)
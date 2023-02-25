from django.contrib.auth import get_user_model
from django_rest_passwordreset.signals import reset_password_token_created      
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from Homemix.settings import DEFAULT_FROM_EMAIL
from .models import User
from dotenv import load_dotenv
load_dotenv()
import os
from mailjet_rest import Client

api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.getenv('MJ_APIKEY_PRIVATE')
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

@receiver(post_save, sender=get_user_model(), dispatch_uid="unique_identifier")
def send_confirmation_email(sender, instance, created, **kwargs):
    print('triggered')
    if created:
        try:
            subject = 'Confirm Your Email Address'
            message = render_to_string('accounts/email_confirmation.html', {
            'user': instance,
            'domain': 'localhost:8000',
            'uid': urlsafe_base64_encode(smart_bytes(instance.pk)),
            'token': default_token_generator.make_token(instance),
        }) 
            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": DEFAULT_FROM_EMAIL,
                            "Name": "Homemix Team"
                        },
                        "To": [
                            {
                                "Email": instance.email,
                                "Name": instance.get_full_name()
                            }
                        ],
                        "Subject": subject,
                        "HTMLPart": message
                    }
                ]
            }

            mailjet.send.create(data=data)
        
        except mailjet.ApiError as e:
            print(f'Mailjet API error: {str(e)}')
            
        except Exception as e:
            print(f'Error sending confirmation email: {e}') 







@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens. Sends an email to the user when a token is created.
    """
    context = {
        'current_user': reset_password_token.user,
        'first_name': reset_password_token.user.first_name,
        'email': reset_password_token.user.email,
        'reset_password_url': f"{instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm'))}?token={reset_password_token.key}"
    }

    email_html_message = render_to_string('accounts\reset_password.html', context)

    subject = "Password Reset for Homemix Account"
    from_email = "noreply@homemix.local"
    to_email = reset_password_token.user.email
    
    msg = EmailMultiAlternatives(subject, email_html_message, from_email, [to_email])
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
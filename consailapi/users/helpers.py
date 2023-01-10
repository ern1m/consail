from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException

from config.celery_app import app
from consailapi.users.models import User


def get_user_data_dict(user: User) -> dict:
    return model_to_dict(user)


@app.task(bind=True, soft_time_timit=21600, time_limit=21610)
def send_email_task(user: User | dict, temp_content):
    try:
        send_mail(
            subject=f"{settings.EMAIL_SUBJECT_PREFIX} {_('Confirmation mail')}",
            from_email=settings.EMAIL_FROM_ADDRESS,
            message=render_to_string(
                "register/emails/send_authorization_message",
                {"context": temp_content, "user": user.get_full_name()},
            ),
            html_message=render_to_string(
                "register/emails/send_authorization_message.html",
                {"context": temp_content, "user": user.get_full_name()},
            ),
            recipient_list=[user.email],
            fail_silently=False,
        )

    except SMTPException:
        raise APIException(
            {
                "non_field_errors": [
                    _("Mail server error occurred. Please contact with administrator.")
                ]
            }
        )

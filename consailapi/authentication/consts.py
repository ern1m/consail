from django.utils.translation import gettext_lazy as _


class AuthenticationMessage:
    INVALID_CREDENTIALS = _("Couldn't validate credentials")
    MISSING_DATA = _('You must include "email" and "password"')
    LOGOUT_SUCCESSFUL = _("You have successfully logged out")

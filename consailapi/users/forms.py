from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email", "password1", "password2")

    # def save(self, *args, **kwargs):
    #     """
    #     Save user. Create if necessary.
    #     :param commit:
    #     :return:
    #     """
    #
    #     self.instance, _c = User.objects.update_or_create(
    #         email=self.cleaned_data["email"],
    #         defaults={
    #             "first_name": self.cleaned_data["first_name"],
    #             "last_name": self.cleaned_data["last_name"],
    #             "username": self.cleaned_data["email"],
    #             "is_active": False,
    #         },
    #     )

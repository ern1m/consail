from copy import deepcopy

from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from consailapi.school.models import Major

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    first_name = forms.CharField(label="First name", required=True)
    last_name = forms.CharField(label="Last name", required=True)
    email = forms.EmailField(label="Email", required=True)
    major = forms.ModelChoiceField(
        label="Major",
        queryset=Major.objects.all(),
        required=False,
    )
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
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
        )

        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
            "username": {"unique": _("This username has already been taken.")},
        }

    def clean_email(self):
        """
        Check if user already exists in database and have activated account
        :return:
        """

        cleaned_data = deepcopy(self.cleaned_data)

        if self.cleaned_data.get("email"):
            cleaned_data["email"] = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=cleaned_data.get("email", "")).exists():
            raise ValidationError(_("Username already exists"))

        return cleaned_data["email"]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"].lower()
        user.username = self.cleaned_data["email"].lower()
        user.is_active = False

        if commit:
            user.save()
        return user

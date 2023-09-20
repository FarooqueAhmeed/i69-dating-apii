from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.forms import CharField, Select, TextInput
from django_otp.forms import OTPAuthenticationFormMixin


class CustomPasswordChangeForm(OTPAuthenticationFormMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(OTPAuthenticationFormMixin, self).__init__(*args, **kwargs)

    otp_device = CharField(required=False, widget=Select)
    otp_token = CharField(
        required=False, widget=TextInput(attrs={"autocomplete": "off"})
    )
    otp_challenge = CharField(required=False)

    def get_user(self):
        err = self.errors.as_data().get("__all__", None)
        print(err)
        return (
            self.request.user
            if self.request.user and self.request.method == "POST"
            else None
        )

    def clean(self):
        self.cleaned_data = super().clean()
        self.clean_otp(self.get_user())
        return self.cleaned_data


class CustomPasswordResetForm(OTPAuthenticationFormMixin, PasswordResetForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(OTPAuthenticationFormMixin, self).__init__(*args, **kwargs)

    otp_device = CharField(required=False, widget=Select)
    otp_token = CharField(
        required=False, widget=TextInput(attrs={"autocomplete": "off"})
    )
    otp_challenge = CharField(required=False)

    def get_user(self):
        if self.request.method == "GET":
            return None
        else:
            return (
                get_user_model()
                .objects.filter(email=self.request.POST["email"])
                .first()
            )

    def clean(self):
        self.cleaned_data = super().clean()
        self.clean_otp(self.get_user())
        return self.cleaned_data

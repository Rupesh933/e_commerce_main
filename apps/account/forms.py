from django.core.exceptions import ValidationError
from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "form-control",
    })
    )

    confirm_password = forms.CharField(
        widget = forms.PasswordInput(attrs={
        "placeholder": "Confirm Password",
        "class": "form-control",
    })
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            "type": 'tel',
            "placeholder": "Enter Your Phone Number",
        })
    )

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "phone_number", "password"]


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "Enter First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter Last Name"
        self.fields['email'].widget.attrs["placeholder"] = "Enter Your Email"

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError(
                "Password does not match",
                code="password_does_not_match"
            )


from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "full_name", "phone_number", "address_line_1", "address_line_2",
            "city", "state", "country", "pincode", "is_default",
        ]
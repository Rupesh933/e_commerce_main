from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from apps.account.models import Account, Address


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Phone Number", "type": "tel"}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email Address"}),
    )

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "phone_number", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Account.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use by another account.")
        return email


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "full_name",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "country",
            "pincode",
            "is_default",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Phone Number", "type": "tel"}),
            "address_line_1": forms.TextInput(attrs={"placeholder": "House number, street name"}),
            "address_line_2": forms.TextInput(attrs={"placeholder": "Apartment, suite, unit (optional)"}),
            "city": forms.TextInput(attrs={"placeholder": "City"}),
            "state": forms.TextInput(attrs={"placeholder": "State"}),
            "country": forms.TextInput(attrs={"placeholder": "Country"}),
            "pincode": forms.TextInput(attrs={"placeholder": "Pincode / ZIP"}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs.update({"placeholder": "Current Password"})
        self.fields["new_password1"].widget.attrs.update({"placeholder": "New Password"})
        self.fields["new_password2"].widget.attrs.update({"placeholder": "Confirm New Password"})


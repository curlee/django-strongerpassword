from django.contrib.auth.forms import (
    PasswordChangeForm as PasswordChangeFormBase
)
from django import forms
from . import validators


class PasswordChangeForm(PasswordChangeFormBase):
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput,
        validators=[validators.HippaValidator()]
    )

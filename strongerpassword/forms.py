from django.contrib.auth.forms import (
    PasswordChangeForm as PasswordChangeFormBase
)
from django import forms
from . import validators


class PasswordChangeForm(PasswordChangeFormBase):
    def __init__(self, *args, **kwargs):
        names = kwargs.pop('names', None)

        super(PasswordChangeForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'] = forms.CharField(
            label='New password',
            widget=forms.PasswordInput,
            validators=[validators.HippaValidator(names=names)]
        )

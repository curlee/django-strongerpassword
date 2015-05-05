from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.core.validators import BaseValidator
from django.utils.translation import ugettext_lazy as _


class HippaValidator(BaseValidator):
    code = 'hippa_error'
    message = _('Your password is not strong enough.')

    def __init__(self, *args, **kwargs):
        self._errors = {}
        self._min_length = kwargs.get('min_length', 6)

        super(HippaValidator, self).__init__(limit_value=None)

    def __call__(self, value):
        self._validate_min_length(value)

        if self._errors:
            raise ValidationError(
                self.message,
                code=self.code,
                params=self._errors
            )

    def _validate_min_length(self, value):
        try:
            MinLengthValidator(self._min_length)(value)
        except Exception, e:
            self._errors[e.code] = _(
                'Your password must be at least %s characters in length.'
            ) % self._min_length

import re
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class HippaValidator(BaseValidator):
    code = 'hippa_error'
    message = _('Your password is not strong enough.')

    def __init__(self, *args, **kwargs):
        self._errors = []
        self._min_length = kwargs.get('length', 6)
        self._min_int_length = kwargs.get('numbers', 1)
        self._min_spec_length = kwargs.get('special', 1)

        super(HippaValidator, self).__init__(limit_value=None)

    def __call__(self, value):
        self._validate_min_length(value)
        self._validate_min_int_length(value)
        self._validate_contains_special_char(value)

        if self._errors:
            raise ValidationError(
                self._errors
            )

    def _validate_min_length(self, value):
        try:
            MinLengthValidator(self._min_length)(value)
        except ValidationError, e:
            self._handle_exception(
                _('Must contain %s or more characters.') % self._min_length,
                e.code
            )

    def _validate_min_int_length(self, value):
        try:
            ContainsNumberValidator()(value)
        except ValidationError, e:
            self._handle_exception(
                ContainsNumberValidator.message % self._min_int_length,
                e.code
            )

    def _validate_contains_special_char(self, value):
        try:
            ContainsSpecialCharValidator()(value)
        except ValidationError, e:
            self._handle_exception(
                ContainsSpecialCharValidator.message % self._min_spec_length,
                e.code
            )

    def _handle_exception(self, message, code):
        if not len(self._errors):
            self._append_error(self.message, self.code)
        self._append_error(message, code)

    def _append_error(self, message, code):
        self._errors.append(
            ValidationError(
                message=message,
                code=code
            )
        )


class ContainsNumberValidator(RegexValidator):
    message = _('Must contain %s or more numbers.')
    regex = re.compile(
        r'[0-9]+'
    )


class ContainsSpecialCharValidator(RegexValidator):
    message = _('Must contain %s or more special characters.')
    code = 'special_chars'
    regex = re.compile(
        r'[$&*]+'
    )

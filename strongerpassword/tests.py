from django.test import TestCase
from .validators import HippaValidator
from django.core.exceptions import ValidationError


class TestHippaValidator(TestCase):
    def setUp(self):
        # these will change as more rules are added
        self.goodpw = 'goodpass'
        self.badpw = 'badpw'
        self.shortpw = 'badpw'

    def test_raise_hippa_error(self):
        self.assertRaises(ValidationError, HippaValidator(), self.badpw)

    def test_hippa_invalid_message(self):
        try:
            HippaValidator()(self.badpw)
        except Exception, e:
            message = e.message

        self.assertEquals(
            message,
            'Your password is not strong enough.'
        )

    def test_raise_hippa_error_shortpw_exception(self):
        try:
            HippaValidator()(self.shortpw)
        except ValidationError, e:
            errors = e.params

        self.assertEquals(
            errors['min_length'],
            'Your password must be at least 6 characters in length.'
        )

    def test_good_password(self):
        error = False

        try:
            HippaValidator()(self.goodpw)
        except ValidationError:
            error = True

        self.assertFalse(error)

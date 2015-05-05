from django.test import TestCase
from .validators import HippaValidator
from django.core.exceptions import ValidationError


class TestHippaValidator(TestCase):
    def setUp(self):
        # these will change as more rules are added
        self.pw_good = 'goodpass1*'
        self.pw_bad = 'a'
        self.pw_tooshort = 'badpw'
        self.pw_nonumber = 'nonumber'
        self.pw_nospecialchars = 'adsfasdfasdf123'

    def test_raise_hippa_error(self):
        self.assertRaises(ValidationError, HippaValidator(), self.pw_bad)

    def test_hippa_invalid_message(self):
        try:
            HippaValidator()(self.pw_bad)
        except Exception, e:
            error = e.error_list

        self.assertEquals(
            error[0].message,
            'Your password is not strong enough.'
        )

    def test_raise_hippa_error_shortpw_exception(self):
        try:
            HippaValidator()(self.pw_tooshort)
        except ValidationError, e:
            error = e.error_list

        self.assertEquals(
            error[1].message,
            'Must contain 6 or more characters.'
        )

    def test_raise_hippa_error_missingint_exception(self):
        try:
            HippaValidator()(self.pw_nonumber)
        except ValidationError, e:
            error = e.error_list

        self.assertEquals(
            error[1].message,
            'Must contain 1 or more numbers.'
        )

    def test_raise_hippa_error_missingspecialchar_exception(self):
        try:
            HippaValidator()(self.pw_nospecialchars)
        except ValidationError, e:
            error = e.error_list

        self.assertEquals(
            error[1].message,
            'Must contain 1 or more special characters.'
        )

    def test_good_password(self):
        error = False

        try:
            HippaValidator()(self.pw_good)
        except ValidationError:
            error = True

        self.assertFalse(error)

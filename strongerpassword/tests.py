import os
from django.test import TestCase
from .validators import HippaValidator
from django.core.exceptions import ValidationError

HERE = os.path.dirname(os.path.realpath(__file__))
TEST_DICT_PATH = os.path.join(HERE, 'test_dictionary')


class TestHippaValidator(TestCase):
    def setUp(self):
        # these will change as more rules are added
        self.pw_good = 'goodpass1*'
        self.pw_bad = 'a'
        self.pw_tooshort = 'short'
        self.pw_nonumber = 'nonumber'
        self.pw_nospecialchars = 'adsfasdfasdf123'
        self.pw_dictionary = 'ESSENTIAL1*'

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

    def test_raise_hippa_error_dictionary_exception(self):
        try:
            HippaValidator(
                dictionary=TEST_DICT_PATH
            )(
                value=self.pw_dictionary
            )
        except ValidationError, e:
            error = e.error_list

        self.assertEquals(
            error[1].message,
            'Must not contain common words.'
        )

    def test_raise_hippa_error_dictionary_exception_withlist(self):
        try:
            HippaValidator(
                dictionary=['elephant',]
            )(
                value='elephant&1'
            )
        except ValidationError, e:
            error = e.error_list

        self.assertEquals(
            error[1].message,
            'Must not contain common words.'
        )

    def test_good_password(self):
        error = False

        try:
            HippaValidator()(self.pw_good)
        except ValidationError, e:
            error = e

        self.assertFalse(error)

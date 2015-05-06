import os
from django.test import TestCase
from django.core.exceptions import ValidationError
from authtools.models import User
from .validators import HippaValidator
from .validators import LengthValidator
from .validators import ContainsNumberValidator
from .validators import ContainsSpecialCharValidator
from .validators import DictionaryValidator
from .validators import NameValidator


HERE = os.path.dirname(os.path.realpath(__file__))
TEST_DICT_PATH = os.path.join(HERE, 'test_dictionary')


class TestHippaValidator(TestCase):
    @property
    def kwargs(self):
        return {
            'length': 6,
            'number': 1,
            'special': 1,
            'dictionary': TEST_DICT_PATH,
            'names': ['foobar']
        }

    def setUp(self):
        # these will change as more rules are added
        self.pw_good = 'goodpass1*'
        self.pw_bad = 'a'
        self.pw_tooshort = 'short'
        self.pw_nonumber = 'nonumber'
        self.pw_nospecialchars = 'adsfasdfasdf123'
        self.pw_dictionary = 'ESSENTIAL1*'
        self.pw_username = 'foobarnamepass1*'

    def test_raise_hippa_error(self):
        self.assertRaises(
            ValidationError,
            HippaValidator(**self.kwargs),
            self.pw_bad
        )

    def test_hippa_invalid_message(self):
        error = False

        try:
            HippaValidator(**self.kwargs)(self.pw_bad)
        except Exception, e:
            error = e.error_list[0].message

        self.assertEquals(
            error,
            HippaValidator.message
        )

    def test_raise_hippa_error_shortpw_exception(self):
        error = False

        try:
            HippaValidator(**self.kwargs)(self.pw_tooshort)
        except ValidationError, e:
            error = e.error_list[1].message

        self.assertEquals(
            error,
            LengthValidator.message % self.kwargs['length']
        )

    def test_raise_hippa_error_missingint_exception(self):
        error = False

        try:
            HippaValidator(**self.kwargs)(self.pw_nonumber)
        except ValidationError, e:
            error = e.error_list[1].message

        self.assertEquals(
            error,
            'Must contain 1 or more numbers.'
        )

    def test_raise_hippa_error_missingspecialchar_exception(self):
        error = False

        try:
            HippaValidator(**self.kwargs)(self.pw_nospecialchars)
        except ValidationError, e:
            error = e.error_list[1].message

        self.assertEquals(
            error,
            'Must contain 1 or more special characters.'
        )

    def test_raise_hippa_error_dictionary_exception(self):
        error = False

        try:
            HippaValidator(**self.kwargs)(
                value=self.pw_dictionary
            )
        except ValidationError, e:
            error = e.error_list[1].message

        self.assertEquals(
            error,
            DictionaryValidator.message
        )

    def test_raise_hippa_error_dictionary_exception_withlist(self):
        kwargs = self.kwargs
        kwargs['dictionary'] = ['elephant']
        error = False

        try:
            HippaValidator(
                **kwargs
            )(
                value='elephant&1'
            )
        except ValidationError, e:
            error = e.error_list[1].message

        self.assertEquals(
            error,
            DictionaryValidator.message
        )

    def test_raise_username_error(self):
        error = False

        try:
            HippaValidator(
                **self.kwargs
            )(self.pw_username)
        except ValidationError, e:
            error = e.error_list[1].message

        self.assertEquals(
            error, NameValidator.message
        )

    def test_good_password(self):
        error = False

        try:
            HippaValidator(**self.kwargs)(self.pw_good)
        except ValidationError, e:
            error = e

        self.assertFalse(error)

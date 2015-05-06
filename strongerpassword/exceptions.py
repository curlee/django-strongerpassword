from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class MissingDictionaryError(ValidationError):
    def __init__(self, **kwargs):
        if not kwargs.get('message'):
            kwargs.update(
                {'message': _('No dictionary supplied to validator.')}
            )

        if not kwargs.get('code'):
            kwargs.update({
                'code': 'missing_dictionary'
            })

        super(MissingDictionaryError, self).__init__(**kwargs)


class MissingNamesError(ValidationError):
    def __init__(self, **kwargs):
        if not kwargs.get('message'):
            kwargs.update(
                {'message': _('No names supplied to validator.')}
            )

        if not kwargs.get('code'):
            kwargs.update({
                'code': 'missing_names'
            })

        super(MissingNamesError, self).__init__(**kwargs)

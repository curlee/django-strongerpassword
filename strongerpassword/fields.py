from django.forms import CharField, PasswordInput
from .validators import HippaValidator


class StrongerPasswordField(CharField):
    default_validators = [
        HippaValidator
    ]

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs["widget"] = PasswordInput(render_value=False)

        super(StrongerPasswordField, self).__init__(*args, **kwargs)

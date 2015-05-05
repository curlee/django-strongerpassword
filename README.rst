=====
Stronger Password
=====

Quick start

1. Add "strongerpassword" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'strongerpassword',
    ]

2. Make use of the StrongerPasswordField form field::

  class Form(forms.Form):
     password = StrongerPasswordField(label='Password')

3. Add settings (optional)

  STRONGER_PASSWORD = {
    'length': 6,
    'numbers': 1,
    'special': 1,
    'dictionary': path/to/dictionary
  }


Build:

    python setup.py sdist
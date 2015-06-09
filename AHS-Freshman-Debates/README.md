# AHS Freshman Debates
Judging App for Albany High School Freshman Renewal Debates.

# TODO
- Redo admin import for new models
- Write tests
- Decide what should be done in admin versus in app.
- Use PEP8
- Decide how to deal with attendance

# Requirements
- [Python](https://www.python.org/downloads/) 3.x

## Available Through PyPi
- [Django](https://www.djangoproject.com/) ([Django](https://pypi.python.org/pypi/Django/))
- Python Social Auth ([python-social-auth](https://pypi.python.org/pypi/python-social-auth/))
- Django Import / Export ([django-import-export](https://pypi.python.org/pypi/django-import-export))
    - Tablib ([tablib](https://pypi.python.org/pypi/tablib)) must currently be installed from Github
      (version on PyPi is 3 years old and does not support Python 3) using `pip install -e
      git+https://github.com/kennethreitz/tablib.git#egg=tablib`

# Setup
- move debates\_site/settings\_secret.py.template to debates\_site/settings\_secret.py
- follow step 1 from the [Google+ Sign in quickstart for Python](https://developers.google.com/+/quickstart/python)
- fill out the client key and secret in the debates\_site/settings\_secret.py file
- ./manage.py syncdb (initialize database tables)

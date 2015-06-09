#!/bin/sh

cd grading

rm db.sqlite3
python manage.py syncdb
python manage.py migrate usermanage
python manage.py migrate lessons
python manage.py migrate allauth.socialaccount
python manage.py loaddata usermanage
python manage.py loaddata lessons

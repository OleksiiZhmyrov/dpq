Django Push Queue Application
------------------------------------------------------------------------------

This application requires Django 1.4 to run.
It is recommended to deploy application inside virtualenv.

Default database is Sqlite but other options are available.
See settings.py for details.



Deployment with Django development server
------------------------------------------------------------------------------
$ cd /some/where
$ virtualenv venv
New python executable in venv/bin/python2.7
Also creating executable in venv/bin/python
Installing setuptools............done.
Installing pip...............done.
$ . venv/bin/activate
(venv)$ pip install Django==1.4
Downloading/unpacking Django==1.4
  Downloading Django-1.4.tar.gz (7.6Mb): 7.6Mb downloaded
  Running setup.py egg_info for package Django

Installing collected packages: Django
  Running setup.py install for Django
    changing mode of build/scripts-2.7/django-admin.py from 644 to 755

    changing mode of /home/zhmyrov/devel/dpq/venv/bin/django-admin.py to 755
Successfully installed Django
Cleaning up...
(venv)$ cd src/
(venv)$ python manage.py runserver
Validating models...

0 errors found
Django version 1.4, using settings 'dpq.settings'
Development server is running at http://127.0.0.1:8000/
Quit the server with CONTROL-C.



Notes
------------------------------------------------------------------------------
  1. Repository contains sample Sqlite database.
  2. Default administrator credentials: admin/admin.
  3. Repository contains Bootstrap and jQuery files.


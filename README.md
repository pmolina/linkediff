linkediff
=========

Diff for LinkedIn

Setup
-----

1. Get the code: `git clone git@github.com:pmolina/linkediff.git`
2. Get [virtualenv](http://www.virtualenv.org/en/latest/) and do a `virtualenv linkediff/`
3. Go to the directory and activate virtualenv with `source bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Copy and edit a new env.py file: `cp linkediff/linkediff/env.py.skeleton linkediff/linkediff/env.py`
6. Run syncdb: `python linkediff/manage.py syncdb`
7. Add `127.0.0.1 linkediff.local` to your /etc/hosts (optional)

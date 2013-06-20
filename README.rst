linkediff
=========

Diff for LinkedIn: create a pool of candidates, compare them in a user friendly environment, made up your mind in a few simple steps, hire the best choice!


First of all
============

Virtualenv
----------

Install last version of virtualenv and virtualenvwrapper::

  $ sudo pip install virtualenv virtualenvwrapper

.. tip::
  Add `. virtualenvwrapper.sh` to your `.bashrc` file to make all
  virtualenvwrapper commands available.

Create a virtualenv::

  $ mkvirtualenv --no-site-packages myenv

.. caution::
  Virutalenvwrapper puts all environments in a directory (usually
  `~/.virtualenvs`), which means that you have a global namespace of
  virtualenvs. A good practice would be to prefix the virtualenv name
  with part of the name of the project to make it unique, something
  like `linkdenv` for linkediff.


Get the code
------------

You already have git, so, let's clone this source::

  $ git clone git@github.com:pmolina/linkediff.git

Or::
  
  $ git clone https://github.com/pmolina/linkediff.git


Activate and Setup requirements
-------------------------------

Activate the environment::

  $ workon myenv

Install requirements::

  $ pip install -r requirements.txt
  
  
Personalize your environment
----------------------------

Copy and edit a new env.py file::

  $ cp linkediff/linkediff/env.py.skeleton linkediff/linkediff/env.py
  

Start your server
-----------------

First sync your db::

  $ python linkediff/manage.py syncdb
  
Start your Django::

  $ manage.py runserver
  
..tip::
  You can add `127.0.0.1 linkediff.local` to your /etc/hosts.
  

Go to your browser and try it yourself.

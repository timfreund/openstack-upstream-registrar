# OpenStack Upstream Registrar

This branch contains a command line script that handles registration of new
Upstream students and mentors.  Students and mentors both submit personal
and professional details via Google Forms, and this script processes those
submissions.

Students are entered into a Trello board and emailed.

Mentors are emailed.

To use:

    $ virtualenv .venv
    $ . .venv/bin/activate
    $ pip install -r requirements.txt
    $ cp config.ini-sample config.ini
    $ # edit config.ini
    $ python register-applicants.py

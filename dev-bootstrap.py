#!/usr/bin/env python

import sys, os
sys.path.append('./upstream')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings
from datetime import datetime, date, timedelta
from registrar.models import *

def create_sessions():
    session_data = [
        {'name': 'Tokyo Summit 2015', 
         'start_date': date(2015, 10, 26),
         'maximum_students': 65},
        {'name': 'Vancouver Summit 2015', 
         'start_date': date(2015, 5, 16),
         'maximum_students': 65},
        {'name': 'Paris Summit 2014', 
         'start_date': date(2014, 11, 1),
         'maximum_students': 65},
        {'name': 'Atlanta Summit 2015', 
         'start_date': date(2014, 5, 10),
         'maximum_students': 35},
    ]
    
    for datum in session_data:
        session = Session()
        for k, v in datum.items():
            setattr(session, k, v)
        Session.save(session)

if __name__ == '__main__':
    create_sessions()


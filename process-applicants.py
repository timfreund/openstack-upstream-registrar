import ConfigParser
import json
import gspread
import requests
import traceback
from trello import TrelloApi
from oauth2client.client import SignedJwtAssertionCredentials

def authorize_gspread_client(credential_file_path):
    with open(credential_file_path, 'r') as cred_file:
        json_key = json.load(cred_file)
        scope = ['https://spreadsheets.google.com/feeds']

        client_email = json_key['client_email']
        private_key = json_key['private_key']
        credentials = SignedJwtAssertionCredentials(client_email, private_key, scope)
        gspread_client = gspread.authorize(credentials)
        return gspread_client

def process_spreadsheet(document_url, gspread_client, row_function, **kwarg):
    spreadsheet = gspread_client.open_by_url(document_url)
    worksheet = spreadsheet.worksheets()[0]

    for index, record in enumerate(worksheet.get_all_records(), start=2):
        if not record.get('upstream-registrar', None):
            try:
                row_function(record, **kwarg)
                worksheet.update_cell(index, 26, 'processed')
            except Exception as e:
                print "Error processing %s" % record['Name']
                traceback.print_exception(Exception, e, None)
        else:
            print("%(Name)s previously processed" % record)

def notify_new_mentor(record, **context):
    subject = "Welcome to OpenStack Upstream mentoring!"
    template = """Hello %(Name)s - 

Thank you for volunteering as a mentor for our OpenStack Upstream students!

We've added you to the mentoring roster, and we will contact you soon with
additional information.  Please reply to this message if you have any
questions or concerns.

In the meantime, please review the information available on the wiki:

https://wiki.openstack.org/wiki/OpenStack_Upstream_Training/Admin

Thanks!

Tim Freund
"""
    send_mail(record, subject, template, **context)

def notify_new_student(record, **context):
    subject = "Welcome to OpenStack Upstream Training!"
    template = """Hello %(Name)s - 

Welcome to OpenStack Upstream Training!  We are looking forward to our
time together in Tokyo.  The objective of the two day session is to
improve your understanding of OpenStack's contribution process and
help you become more effective at merging code in OpenStack. The
training is designed to be practical, it begins *now* before and will
continue after, with mentoring sessions until your first contribution
is completed.

If you haven't done it already, get familiar with OpenStack Upstream
Training logistics[1], course objectives, the schedule[2], and
pre-requisites[3].

[1] https://wiki.openstack.org/wiki/OpenStack_Upstream_Training
[1] https://wiki.openstack.org/wiki/OpenStack_Upstream_Training/Info#Objectives
[2] https://wiki.openstack.org/wiki/OpenStack_Upstream_Training/Info#Course_Outline
[3] https://wiki.openstack.org/wiki/OpenStack_Upstream_Training/Info#Prerequisites

Please start engaging with your mentor by replying to this message,
explaining what you would like to work on and what your personal
objectives are for this class. The mentor will help you select a low
hanging fruit bug to fix and send you further instructions.

Don't hesitate to ask if you have questions regarding the training
program.  We are here to help you!

Reply to this email if you have any questions.  Talk to you soon!

Tim Freund
"""
    
    send_mail(record, subject, template, **context)

def send_mail(record, subject, template, **context):
    mailgun_url = context['mailgun_url']
    mailgun_key = context['mailgun_key']
    sender = context['mail_sender']
    cc = context['mail_cc']

    requests.post(
        mailgun_url,
        auth=("api", mailgun_key), 
        data={"from": sender,
              "to": [record['Email']],
              'cc': [cc],
              "subject": subject,
              "text": template % record})

def process_new_student(record, **context):
    print("processing new student %(Name)s (%(Email)s)" % record)
    trello = context['trello']
    board_id = context['trello_board_id']

    list_id = None
    for l in trello.boards.get_list(board_id):
        if l['name'] == 'Applicants':
            list_id = l['id']
            break

    card_title = "%(Name)s, %(Title)s @ %(Organization)s" % record
    card_description_list = []
    for k, v in record.items():
        card_description_list.append("%s: %s" % (k, v))
    card_description = "\n\n".join(card_description_list)
    card = trello.lists.new_card(list_id, card_title, card_description)

    notify_new_student(record, **context)

def process_new_mentor(record, **kwarg):
    print("processing new mentor %(Name)s (%(Email)s)" % record)
    notify_new_mentor(record, **context)

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read("config.ini")

    credential_file_path = config.get('gspread', 'credential_file_path')
    student_url = config.get('gspread', 'student_url')
    mentor_url = config.get('gspread', 'mentor_url')

    trello_app_key = config.get('trello', 'trello_app_key')
    trello_board_id = config.get('trello', 'trello_board_id')
    trello_token = config.get('trello', 'trello_token')

    if trello_token is None:
        print "go to https://trello.com/1/authorize?key=%s&name=openstack-upstream-registrar&expiration=never&response_type=token&scope=read,write" % (trello_app_key)
        import sys
        trello_token = sys.stdin.readline().strip()
    
    gspread_client = authorize_gspread_client(credential_file_path)
    context = {
        'mailgun_url': config.get('mail', 'mailgun_url'),
        'mailgun_key': config.get('mail', 'mailgun_key'),
        'mail_sender': config.get('mail', 'mail_sender'),
        'mail_cc': config.get('mail', 'mail_cc'),
        'trello': TrelloApi(trello_app_key, token=trello_token),
        'trello_board_id': trello_board_id,
    }
    process_spreadsheet(mentor_url, gspread_client, process_new_mentor, **context)
    process_spreadsheet(student_url, gspread_client, process_new_student, **context)

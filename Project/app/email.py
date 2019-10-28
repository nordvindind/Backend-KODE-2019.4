import os
from flask_mail import Message
from . import celery
from sps import app
from app import mail


@celery.task
def send_async_email(email_data):
    ''' Background task to send an email with Flask-Mail. '''
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    # Celery needs context
    with app.app_context():
        mail.send(msg)


def send_ticker_email(s_email, ticker):
    ''' Func to send mail about notifications.
        Can be modified to accept templates for any type of mails. '''
    email_data = {
        'subject': 'Changes on {ticker} price'.format(ticker=ticker),
        'to': s_email,
        'body': "{to}, price on {ticker} changed. Wake up.".format(to=s_email, ticker=ticker)
    }
    # Fot development and testing purposes.
    print(email_data)
    # send_async_email(email_data)

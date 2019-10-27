from . import celery
from sps import app


@celery.task
def send_ticker_email(to, ticker, **kwargs):
    mail = "{to}, price on {ticker} changed. Wake up.".format(to=to, ticker=ticker)
    print(mail)
    # app = current_app._get_current_object()
    # msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
    #               sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    # msg.body = render_template(template + '.txt', **kwargs)
    # msg.html = render_template(template + '.html', **kwargs)
    # send_async_email.delay(msg)

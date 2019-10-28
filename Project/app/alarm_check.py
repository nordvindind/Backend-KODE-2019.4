from datetime import timedelta
from operator import attrgetter
from sqlalchemy import distinct
from sps import app
from app import db
from app.models import Subscribers, Subscriptions
from app.email import send_ticker_email
from app.api.queries import get_ticker_prices
from . import celery


@celery.task()
def check_alarms():
    ''' Periodic task to alarm subscribers about changes '''
    ''' To make it better, DB structure should be trigger price + condition
        Current structre allows easier control of subscription count by ticker,
        not notifying users '''
    # We need context because celery works outside of app
    with app.app_context():
        subscriptions = Subscriptions.query.all()
        # I do not understand why I couldn't use 1 query.
        # I guess DB is faster to get only tickers
        subscription_tickers = Subscriptions.query.distinct(Subscriptions.ticker).all()

    # check if subscriptions exist
    if len(subscription_tickers) > 0:
        # extracting distinct tickers to get min/max prices
        tuple_of_tickers = tuple(map(attrgetter('ticker'), subscription_tickers))
        prices_for_tickers = get_ticker_prices(tuple_of_tickers)

        # Cheking every subscription
        for subscription in subscriptions:
            # I know, it's handicapble, But I do not have time
            try:
                s_min_price = float(subscription.min_price)
            except:
                s_min_price = 0
            try:
                s_max_price = float(subscription.max_price)
            except:
                s_max_price = 16000000
            # variable for email sending check
            # It was 11th hour straight of coding.
            # Just accept naming
            is_to_send_email = False
            if s_min_price > float(prices_for_tickers[subscription.ticker]["low"]):
                is_to_send_email = True
                subscription.min_price = None
            if s_max_price < float(prices_for_tickers[subscription.ticker]["high"]):
                is_to_send_email = True
                subscription.max_price = None
            # Facepalm, but I do not have time to fix it
            # Sending email, if there is cause
            if is_to_send_email:
                with app.app_context():
                    # getting email for particular subscription
                    # I tried join, but celery doesn't understand how to deal with it
                    s_email = Subscribers.query.get(subscription.subscriber_id)
                    send_ticker_email(s_email, subscription.ticker)
                    # If min and max triggers are empty, we remove alarm
                    if subscription.min_price is None and subscription.max_price is None:
                        db.session.delete(subscription)
                        db.session.commit()
    return None

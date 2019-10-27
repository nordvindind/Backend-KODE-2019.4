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
    with app.app_context():
        subscriptions = Subscriptions.query.all()
        # I do not understand why I couldn't use 1 query.
        # I guess DB is faster
        subscription_tickers = Subscriptions.query.distinct(Subscriptions.ticker).all()

    tuple_of_tickers = tuple(map(attrgetter('ticker'), subscription_tickers))
    if len(tuple_of_tickers) > 0:
        prices_for_tickers = get_ticker_prices(tuple_of_tickers)

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
            if s_min_price > float(prices_for_tickers[subscription.ticker]["low"]):
                is_to_send_email = True
                subscription.min_price = None

            if s_max_price < float(prices_for_tickers[subscription.ticker]["high"]):
                is_to_send_email = True
                subscription.max_price = None
                # Facepalm, but I do not have time to fix it
            if is_to_send_email:
                with app.app_context():
                    s_email = Subscribers.query.get(subscription.subscriber_id)
                    send_ticker_email(s_email, subscription.ticker)
                    if subscription.min_price is None and subscription.max_price is None:
                        db.session.delete(subscription)
                        db.session.commit()
    return None

import os
from decimal import *
from flask import jsonify, request
from app import db
from app.models import Subscribers, Subscriptions
from . import bp
from .queries import check_stocks_ticker


@bp.route('/subscription', methods=['GET', 'POST', "DELETE"])
def subscription_managment():
    # I don't know why you need to accept same data as arguments and as JSON
    # Ok, I will do it.
    data = request.get_json() or {}

    email = request.args.get("email", None, type=str)
    if "email" in data and data["email"]:
        email = data["email"]
    if email:
        email = email.lower()

        ticker = request.args.get("ticker", None, type=str)
        if "ticker" in data and data["ticker"]:
            ticker = data["ticker"]
        if ticker:
            ticker = ticker.upper()

        # It's price and we want 0, not 5.5511151231257827e-017
        # So, str to store and conversion to decimals
        min_price = request.args.get("min_price", None, type=str)
        max_price = request.args.get("max_price", None, type=str)
        if "min_price" in data and data["min_price"]:
            min_price = data["min_price"]
        if "max_price" in data and data["max_price"]:
            max_price = data["max_price"]
        # If we can converse to float, we can do it with decimals
        try:
            float(min_price)
        except:
            min_price = None
        try:
            float(max_price)
        except:
            max_price = None

        # Getting subscriber object with data from db
        subscriber = Subscribers.query.filter_by(email=email).first()
        # Check if subscriber exists
        if subscriber is None:
            # if not, create new one
            # it's bad order of action
            # I need time to change it
            # but it's good enough
            subscriber = Subscribers(
                email=email
            )
            db.session.add(subscriber)
            db.session.flush()
        # GET is only for testing and development purposes
        if request.method == "GET" and os.environ["FLASK_ENV"] == "development":
            data = Subscribers.to_collection_dict(Subscribers.query.filter_by(id=subscriber.id))
            return jsonify(data)

        # Creating and updating a subscription or removing all subscriptions
        if request.method == "POST":
            if ticker and check_stocks_ticker(ticker):
                if min_price or max_price:
                    # check if subscription entry with given ticker exists
                    subscription = Subscriptions.query.filter(
                        Subscriptions.subscriber_id == subscriber.id,
                        Subscriptions.ticker == ticker
                    ).first()
                    # Changing/creating subscription
                    if subscription:
                        subscription.min_price = min_price
                        subscription.max_price = max_price
                    else:
                        if subscriber.subscription_count == 5:
                            return "Limit riched: 5 subscriptions per email"
                        new_subscription = Subscriptions(
                            subscriber_id=subscriber.id,
                            ticker=ticker,
                            min_price=min_price,
                            max_price=max_price
                        )
                        db.session.add(new_subscription)
                    db.session.flush()
                    subscriber.update_subscription_count()
                    db.session.commit()
                else:
                    return "400"
            else:
                # we can just drop subscriber row, because relationship
                db.session.delete(subscriber)
                db.session.commit()
        # removing only 1 subscription
        if request.method == "DELETE":
            if ticker:
                # Removing subscription that doesn't exist causes error
                # We need to check if it exists
                subscription = Subscriptions.query.filter(
                    Subscriptions.subscriber_id == subscriber.id,
                    Subscriptions.ticker == ticker
                ).first()
                if subscription:
                    db.session.delete(subscription)
                else:
                    return "404"
        return "200"
    return "400"

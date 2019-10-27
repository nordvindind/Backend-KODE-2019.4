from datetime import datetime
from app import db


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query):
        resources = query.paginate(1, 6, False)
        data = {
            'items': [item.to_dict() for item in resources.items]
        }
        return data


class Subscriptions(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscribers.id'), nullable=True)
    ticker = db.Column(db.String(8), nullable=False)
    min_price = db.Column(db.String(32), nullable=True)
    max_price = db.Column(db.String(32), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # JSON convert for API
    def to_dict(self):
        data = {
            'id': self.id,
            'ticker': self.ticker,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'created_at': self.created_at
        }
        return data

class Subscribers(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    subscriptions = db.relationship(
        'Subscriptions', cascade="all,delete",
        backref='subscribers', lazy='dynamic'
    )
    subscription_count = db.Column(db.Integer, default=0, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return self.email

    def get_subscriptions(self):
        return self.subscriptions.all()

    def update_subscription_count(self):
        self.subscription_count = self.subscriptions.count()

    # JSON convert for API
    def to_dict(self):
        data = {
            'id': self.id,
            'email': self.email,
            'subscription_count': self.subscription_count,
            # 'subscriptions': self.get_subscriptions().to_dict(),

            'subscriptions': Subscriptions.to_collection_dict(self.subscriptions),
            'created_at': self.created_at
        }
        return data

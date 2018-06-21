from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, \
    SignatureExpired


db = SQLAlchemy()


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    user = db.relationship("User", backref=db.backref("admin"), uselist=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @staticmethod
    def hash_password(password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=300):
        s = Serializer(db.app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"id": self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(db.app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        admin = Admin.query.get(data["id"])
        return admin

    def __init__(self, user, password):
        self.user = user
        self.password_hash = self.hash_password(password)

    def __repr__(self):
        return "<Admin {} ({})".format(self.id, self.user.email)

    def dump(self):
        """
        Dump Admin object as json
        :return: Dictionary of publicly available admin information
        """
        return {
            "admin_id":   self.id,
            "user_id":    self.user.id
        }


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("accounts", lazy="dynamic"))

    def __init__(self, name, user):
        self.name = name
        self.user = user

    def __repr__(self):
        return "<Account {} ({})>".format(self.id, self.user.id)

    def balance(self):
        """
        :return: returns account balance as float.
        """
        return round(sum([transaction.balance_change for transaction in self.transactions]), 2)

    def card_shas(self):
        """
        Get list of card SHAs associated with the account
        :return: List of card SHAs
        """
        return [card.sha for card in self.cards]

    def dump(self):
        """
        :return: Returns all account information.
        """
        return {
            "account_id":   self.id,
            "balance":      self.balance(),
            "card_shas":    self.card_shas(),
            "name":         self.name,
            "user_id":      self.user.id
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    phone = db.Column(db.String(20))

    def __init__(self, name, email, phone=""):
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return "<User {} ({})>".format(self.id, self.name)

    def balance(self):
        """
        :return: Returns users balance as float.
        """
        return round(sum([transaction.balance_change for transaction in self.transactions]), 2)

    def dump(self):
        """
        :return: Returns all user information.
        """
        return {
            "user_id":  self.id,
            "name":     self.name,
            "email":    self.email,
            "phone":    self.phone
        }


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    sha = db.Column(db.String(128), nullable=False, unique=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    account = db.relationship("Account", backref=db.backref("cards", lazy="dynamic"))

    def __init__(self, name, sha, account=None):
        self.name = name
        self.sha = sha
        self.account = account

    def __repr__(self):
        return "<Card {} ({})>".format(self.sha, self.name)

    def dump(self):
        """
        :return: Returns all card information.
        """
        card = {
            "card_sha": self.sha,
            "name":     self.name,
        }
        if not self.account:
            card["account_id"] = 0
        else:
            card["account_id"] = self.account.id
        return card


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    sha = db.Column(db.String(128), nullable=False, unique=True)
    type = db.Column(db.Integer)

    def __init__(self, name, sha, register_type=0):
        self.name = name
        self.sha = sha
        self.type = register_type

    def __repr__(self):
        return "<Register {} ({})>".format(self.sha, self.name)

    def dump(self):
        """
        :return: Returns all register information.
        """
        return {
            "register_sha": self.sha,
            "name":         self.name,
            "type":         self.type
        }


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance_change = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    account = db.relationship("Account", backref=db.backref("transactions", lazy="dynamic"))
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"))
    card = db.relationship("Card", backref=db.backref("transactions", lazy="dynamic"))
    register_id = db.Column(db.Integer, db.ForeignKey("register.id"))
    register = db.relationship("Register", backref=db.backref("transactions", lazy="dynamic"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("transactions", lazy="dynamic"))

    def __init__(self, user, account, card, register, balance_change):
        self.user = user
        self.account = account
        self.card = card
        self.register = register
        self.balance_change = balance_change
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return "<Transaction {}>".format(self.id)

    def dump(self):
        """
        :return: Returns all transaction information.
        """
        return {
            "account_id":       self.account.id,
            "balance_change":   self.balance_change,
            "card_sha":         self.card.sha,
            "register_sha":     self.register.sha,
            "transaction_id":   self.id,
            "timestamp":        self.timestamp.isoformat()
        }

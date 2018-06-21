from flask import url_for
from .utils import MasonObject, AccountId, CardSHA, RegisterSHA, status
from server.config import base_url
from server.db.api import Account, Card, Register, User, Transaction


class TransactionObject(MasonObject):
    def __init__(self, **kwargs):
        super(TransactionObject, self).__init__(**kwargs)
        self["account"] = AccountId(self.pop("account_id"))
        self["card"] = CardSHA(self.pop("card_sha"))
        self["register"] = RegisterSHA(self.pop("register_sha"))
        self.add_namespace("cr", base_url)
        self.add_control_self("/transactions/{}".format(self.get("transaction_id", 0)))
        self.add_control_create(
            "cr:create-transaction",
            "Create new transaction",
            "/transactions",
            url_for("static", filename="transaction-post.json")
        )


def get(transaction_id):
    transaction, code, message = Transaction.get(transaction_id)
    if not transaction:
        return status(code, message)
    return TransactionObject(**transaction.dump())


def get_all(page=1):
    return generate_response(Transaction.get_all(page)[0])


def get_by_account(account_id, page=1):
    account, code, message = Account.get(account_id)
    if not account:
        return status(code, message)
    return generate_response(Transaction.get_by_account(account.id, page)[0])


def get_by_card(card_sha, page=1):
    card, code, message = Card.get(sha=card_sha)
    if not card:
        return status(code, message)
    return generate_response(Transaction.get_by_card(card.id, page)[0])


def get_by_register(register_sha, page=1):
    register, code, message = Register.get(sha=register_sha)
    if not register:
        return status(code, message)
    return generate_response(Transaction.get_by_register(register.id, page)[0])


def get_by_user(user_id, page=1):
    user, code, message = User.get(user_id)
    if not user:
        return status(code, message)
    return generate_response(Transaction.get_by_user(user.id, page)[0])


def post(transaction):
    card, code, message = Card.get(sha=transaction.get("card_sha"))
    register, code, message = Register.get(sha=transaction.get("register_sha"))
    if not card or not register:
        return status(412, message)

    parameters = {
        "balance_change": transaction.get("balance_change"),
        "card_id": card.id,
        "register_id": register.id
    }
    transaction, code, message = Transaction.create(**parameters)
    if not transaction:
        return status(code, message)
    return TransactionObject(**transaction.dump()), code


def generate_response(result):
    response = {
        "count":    result.total,
        "results":  [TransactionObject(**transaction.dump()) for transaction in result.items]
    }
    if result.has_next:
        response["next"] = "{}/transactions/?page={}".format(base_url, result.next_num)
    if result.has_prev:
        response["previous"] = "{}/transactions/?page={}".format(base_url, result.prev_num)
    return response

from flask import url_for
from .utils import MasonObject, CardSHA, UserId, status
from server.config import base_url
from server.db.api import Account


class AccountObject(MasonObject):
    def __init__(self, **kwargs):
        super(AccountObject, self).__init__(**kwargs)
        account_id = self.get("account_id", 0)
        self["user"] = UserId(self.pop("user_id", 0))
        self["cards"] = [CardSHA(sha) for sha in self.pop("card_shas", [])]
        self.add_namespace("cr", base_url)
        self.add_control_self("/accounts/{}".format(account_id))
        self.add_control_create(
            "cr:create-account",
            "Create new account",
            "/accounts",
            url_for("static", filename="account-post.json")
        )
        self.add_control_edit(
            "cr:edit-account",
            "Edit this account",
            "/accounts/patch/{}".format(account_id),
            url_for("static", filename="account-patch.json")
        )
        self.add_control_delete("cr:delete-account", "Delete this account", "/accounts/delete/{}".format(account_id))
        self.add_control("cr:account-transactions",
                         title="Get transactions of this account",
                         method="GET",
                         href="/transactions/account/{}".format(account_id))


def get(account_id):
    account, code, message = Account.get(account_id=account_id)
    if not account:
        return status(code, message)
    return AccountObject(**account.dump())


def get_all():
    return [AccountObject(**account.dump()) for account in Account.get_all()[0]]


def patch(account_id, account):
    old_account, code, message = Account.get(account_id=account_id)
    if not old_account:
        return status(code, message)
    account, code, message = Account.edit(old_account.id, **account)
    if not account:
        return status(code, message)
    return AccountObject(**account.dump())


def post(account):
    account, code, message = Account.create(**account)
    if not account:
        return status(code, message)
    return AccountObject(**account.dump()), code


def delete(account_id):
    account, code, message = Account.get(account_id=account_id)
    if account:
        success, code, message = Account.delete(account.id)
    return status(code, message)

from flask import url_for
from .utils import MasonObject, AccountId, status
from server.config import base_url
from server.db.api import User


class UserObject(MasonObject):
    def __init__(self, **kwargs):
        super(UserObject, self).__init__(**kwargs)
        user_id = self.get("user_id", 0)
        self["accounts"] = [AccountId(account_id) for account_id in self.pop("account_ids", [])]
        self.add_namespace("cr", base_url)
        self.add_control_self("/users/{}".format(user_id))
        self.add_control_create(
            "cr:create-user",
            "Create new user",
            "/users",
            url_for("static", filename="user-post.json")
        )
        self.add_control_edit(
            "cr:edit-user",
            "Edit this user",
            "/users/patch/{}".format(user_id),
            url_for("static", filename="user-patch.json")
        )
        self.add_control_delete("cr:delete-user", "Delete this user", "/users/delete/{}".format(user_id))
        self.add_control("cr:user-transactions",
                         title="Get transactions of this user",
                         method="GET",
                         href="/transactions/user/{}".format(user_id))


def get(user_id):
    user, code, message = User.get(user_id=user_id)
    if not user:
        return status(code, message)
    return UserObject(**user.dump())


def get_all():
    return [UserObject(**user.dump()) for user in User.get_all()[0]]


def patch(user_id, user):
    old_user, code, message = User.get(user_id=user_id)
    if not old_user:
        return status(code, message)
    user, code, message = User.edit(old_user.id, **user)
    if not user:
        return status(code, message)
    return UserObject(**user.dump())


def post(user):
    user, code, message = User.create(**user)
    if not user:
        return status(code, message)
    return UserObject(**user.dump()), code


def delete(user_id):
    user, code, message = User.get(user_id=user_id)
    if user:
        success, code, message = User.delete(user.id)
    return status(code, message)

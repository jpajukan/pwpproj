from flask import url_for
from .utils import MasonObject, status
from server.config import base_url
from server.db.api import Register


class RegisterObject(MasonObject):
    def __init__(self, **kwargs):
        super(RegisterObject, self).__init__(**kwargs)
        sha = self.get("register_sha", "0")
        self.add_namespace("cr", base_url)
        self.add_control_self("/registers/{}".format(sha))
        self.add_control_create(
            "cr:create-register",
            "Create new register",
            "/registers",
            url_for("static", filename="register-post.json")
        )
        self.add_control_edit(
            "cr:edit-register",
            "Edit this register",
            "/registers/patch/{}".format(sha),
            url_for("static", filename="register-patch.json")
        )
        self.add_control_delete("cr:delete-register", "Delete this register", "/registers/delete/{}".format(sha))
        self.add_control("cr:register-transactions",
                         title="Get transactions of this register",
                         method="GET",
                         href="/transactions/register/{}".format(sha))


def get(register_sha):
    register, code, message = Register.get(sha=register_sha)
    if not register:
        return status(code, message)
    return RegisterObject(**register.dump())


def get_all():
    return [RegisterObject(**register.dump()) for register in Register.get_all()[0]]


def patch(register_sha, register):
    old_register, code, message = Register.get(sha=register_sha)
    if not old_register:
        return status(code, message)
    paramaters = {
        "name": register.get("name"),
        "register_type": register.get("type")
    }
    register, code, message = Register.edit(old_register.id, **paramaters)
    if not register:
        return status(code, message)
    return RegisterObject(**register.dump())


def post(register):
    paramaters = {
        "name": register.get("name"),
        "sha": register.get("register_sha"),
        "register_type": register.get("type")
    }
    register, code, message = Register.create(**paramaters)
    if not register:
        return status(code, message)
    return RegisterObject(**register.dump()), code


def delete(register_sha):
    register, code, message = Register.get(sha=register_sha)
    if register:
        success, code, message = Register.delete(register.id)
    return status(code, message)

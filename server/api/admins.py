from flask import url_for
from .utils import MasonObject, UserId, status
from server.config import base_url
from server.db.api import Admin


class AdminObject(MasonObject):
    def __init__(self, **kwargs):
        super(AdminObject, self).__init__(**kwargs)
        admin_id = self.get("admin_id", 0)
        self["user"] = UserId(self.pop("user_id", 0))
        self.add_namespace("cr", base_url)
        self.add_control_self("/admins/{}".format(admin_id))
        self.add_control_create(
            "cr:create-admin",
            "Create new admin",
            "/admins",
            url_for("static", filename="admin-post.json")
        )
        self.add_control_edit(
            "cr:edit-admin",
            "Edit this admin",
            "/admins/patch/{}".format(admin_id),
            url_for("static", filename="admin-patch.json")
        )
        self.add_control_delete("cr:delete-admin", "Delete this admin", "/admins/delete/{}".format(admin_id))


def get(admin_id):
    admin, code, message = Admin.get(admin_id=admin_id)
    if not admin:
        return status(code, message)
    return AdminObject(**admin.dump())


def get_all():
    return [AdminObject(**admin.dump()) for admin in Admin.get_all()[0]]


def patch(admin_id, password):
    old_admin, code, message = Admin.get(admin_id=admin_id)
    if not old_admin:
        return status(code, message)
    admin, code, message = Admin.edit(old_admin.id, **password)
    if not admin:
        # Note: this line should never be reached, as bad requests are already caught by schema validation
        return status(code, message)
    return AdminObject(**admin.dump())


def post(admin):
    admin, code, message = Admin.create(**admin)
    if not admin:
        return status(code, message)
    return AdminObject(**admin.dump()), code


def delete(admin_id):
    admin, code, message = Admin.get(admin_id=admin_id)
    if admin:
        success, code, message = Admin.delete(admin.id)
    return status(code, message)

from flask import url_for
from .utils import MasonObject, AccountId, status
from server.config import base_url
from server.db.api import Card


class CardObject(MasonObject):
    def __init__(self, **kwargs):
        super(CardObject, self).__init__(**kwargs)
        sha = self.get("card_sha", "0")
        self["account"] = AccountId(self.pop("account_id", 0))
        self.add_namespace("cr", base_url)
        self.add_control_self("/cards/{}".format(sha))
        self.add_control_create(
            "cr:create-card",
            "Create new card",
            "/cards",
            url_for("static", filename="card-post.json")
        )
        self.add_control_edit(
            "cr:edit-card",
            "Edit this card",
            "/cards/patch/{}".format(sha),
            url_for("static", filename="card-patch.json")
        )
        self.add_control_delete("cr:delete-card", "Delete this card", "/cards/delete/{}".format(sha))
        self.add_control("cr:card-transactions",
                         title="Get transactions of this card",
                         method="GET",
                         href="/transactions/card/{}".format(sha))


def get(card_sha):
    card, code, message = Card.get(sha=card_sha)
    if not card:
        return status(code, message)
    return CardObject(**card.dump())


def get_all():
    return [CardObject(**card.dump()) for card in Card.get_all()[0]]


def get_unassigned():
    return [CardObject(**card.dump()) for card in Card.get_unassigned()[0]]


def patch(card_sha, card):
    old_card, code, message = Card.get(sha=card_sha)
    if not old_card:
        return status(code, message)

    card, code, message = Card.edit(old_card.id, **card)
    if not card:
        return status(code, message)
    return CardObject(**card.dump())


def post(card):
    parameters = {
        "name": card.get("name"),
        "sha": card.get("card_sha"),
        "account_id": card.get("account_id")
    }
    card, code, message = Card.create(**parameters)
    if not card:
        return status(code, message)
    return CardObject(**card.dump()), 201


def delete(card_sha):
    card, code, message = Card.get(sha=card_sha)
    if card:
        success, code, message = Card.delete(card.id)
    return status(code, message)




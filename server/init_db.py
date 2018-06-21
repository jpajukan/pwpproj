import logging

from hashlib import sha256
from server.app import init_app, init_db
from server.db.api import *

logger = logging.getLogger(__name__)

USERS = [
    ("Matti Matikainen", "matti@matikainen.fi", "0501234567"),
    ("Mervi Matikainen", "mervi@matikainen.fi", "0509894172"),
    ("Heikki Herranen", "heikki@herranen.com", "0400123123"),
    ("Touko Pekkala", "toukopouko@example.com", None),
    ("Päivi Lipponen", "paevi@jippii.fi", "0401231231")
]

ACCOUNTS = [
    ("Ruokatili", 1),
    ("Viinatili", 1),
    ("Ruokatili", 2),
    ("Säästötili", 3),
    ("Salatili", 4)
]

CARDS = [
    ("Opiskelijakortti", 1),
    ("Kännykkä", 1),
    ("Opiskelijakortti", 2),
    ("Opiskelijakortti", 3),
    ("Kännykkä", 4),
    ("Opiskelijakortti", 5),
    ("Orpokortti", 0)
]

REGISTERS = [
    ("Kahvihuone", 0),
    ("Kiltahuone", 0),
    ("Admin", 1)
]

TRANSACTIONS = [
    (1, 3, 10.0),
    (2, 3, 1.0),
    (3, 3, 100.0),
    (4, 3, 20.0),
    (5, 3, 30.0),
    (6, 3, 50.0),
    (1, 1, -11.0),
    (3, 2, -80.5),
    (4, 1, -12.6),
    (4, 2, -4.0),
    (5, 2, -5.2),
    (5, 1, -15.0),
    (5, 1, -3.0),
    (6, 3, -10.6),
    (6, 1, -2.6),
    (6, 2, -30.1)
]


def reset_db(db):
    logger.info("Dropping all the tables from the test database")
    db.drop_all()
    logger.info("Creating new tables for the test database")
    db.create_all()


def create_test_users(users=USERS):
    logger.info("Creating test users")
    for name, email, phone in users:
        user, code, message = User.create(name, email, phone)
        if user:
            logger.info("Created test user {} with id {}".format(name, user.id))
        else:
            logger.error("Failed to create test user {}. Return code: {} Message: {}".format(
                name, code, message
            ))


def create_test_accounts(accounts=ACCOUNTS):
    logger.info("Creating test accounts")
    for name, user_id in accounts:
        account, code, message = Account.create(name, user_id)
        if account:
            logger.info("Created test account {} with id {}".format(name, account.id))
        else:
            logger.error("Failed to create test account {}. Return code: {} Message: {}".format(
                name, code, message
            ))


def create_test_cards(cards=CARDS):
    logger.info("Creating test cards")
    for name, account_id in cards:
        sha = sha256((name + str(account_id)).encode()).hexdigest()
        card, code, message = Card.create(name, sha, account_id)
        if card:
            logger.info("Created test card {} with id {}".format(name, card.id))
        else:
            logger.error("Failed to create test card {}. Return code: {} Message: {}".format(
                name, code, message
            ))


def create_test_registers(registers=REGISTERS):
    logger.info("Creating test registers")
    for name, register_type in registers:
        sha = sha256((name + str(register_type)).encode()).hexdigest()
        register, code, message = Register.create(name, sha, register_type)
        if register:
            logger.info("Created test register {} with id {}".format(name, register.id))
        else:
            logger.error("Failed to create test register {}. Return code: {} Message: {}".format(
                name, code, message
            ))


def create_test_transactions(transactions=TRANSACTIONS):
    logger.info("Creating test transactions")
    for card_id, register_id, balance_change in transactions:
        transaction, code, message = Transaction.create(card_id, register_id, balance_change)
        if transaction:
            logger.info("Created test transaction with id {}".format(transaction.id))
        else:
            logger.error("Failed to create test transaction. Return code: {} Message: {}".format(
                code, message
            ))


def create_admin(name="admin", email="admin@localhost", phone=None, password="adminadmin"):
    logger.info("Creating test admin")
    user, code, message = User.create(name, email, phone)
    admin, code, message = Admin.create(user.id, password)
    if admin:
        logger.info("Created test admin {} with id {}".format(name, admin.id))
    else:
        logger.error("Failet to create test admin {}. Return code: {} Message: {}".format(
            name, code, message
        ))


def main():
    db = init_db(init_app(add_api=False).app)
    reset_db(db)
    create_test_users()
    create_test_registers()
    create_test_accounts()
    create_test_cards()
    create_test_transactions()
    create_admin()


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    main()

from sys import maxsize
from server.db import models
from sqlalchemy.exc import DataError, IntegrityError


def commit(session):
    try:
        session.commit()
        return True, 200, ""
    except DataError:
        # Invalid value
        session.rollback()
        return False, 400, "Data constraint failed"
    except IntegrityError:
        # Invalid value
        session.rollback()
        return False, 409, "Integrity constraint failed"


class Account:
    @staticmethod
    def get(account_id=1):
        """
        Get account object with given account id
        :param int account_id: Id of the account as integer.
        :return: If account id is found returns the account object, OK code and message.
            Otherwise returns none, error code and message.
        """
        account = models.Account.query.get(account_id)
        if account:
            return account, 200, "OK"
        return None, 404, "No such account"

    @staticmethod
    def get_all():
        """
        Get all account objects as list.
        :return: returns list of all account objects, OK code and message.
        """
        return models.Account.query.all(), 200, "OK"

    @staticmethod
    def create(name, user_id):
        """
        Creates account object with given name for given user.
        :param str name: Name of the account. Must be unique within user.
        :param int user_id: Id of the user of the account
        :return: If user id is valid and name is unique within user returns new account, success code and message.
            Otherwise returns none, error code and message.
        """
        if not name:
            return None, 400, "Name must not be empty"
        user, code, message = User.get(user_id)
        if not user:  # No such user
            return user, 412, message

        if models.Account.query.filter_by(name=name, user=user).first():
            return None, 409, "Name must be unique within user"

        account = models.Account(name, user)
        session = models.db.session
        session.add(account)
        result, code, message = commit(session)
        if result:
            return account, 201, "Account created"
        return None, code, message

    @staticmethod
    def edit(account_id, name="", user_id=-1):
        """
        Edits account with given id. If name and/or user is given it will become new name/user. If name and or user is
        not given: they will remain the same.
        :param int account_id: Id of the account as integer.
        :param str name: New name of the account as string. Must be unique within user.
        :param int user_id: Id of the new user of the account as integer. User must not have
        account with same name.
        :return: If name for user is unique returns edited account object, success code and message.
            if object is not edited or name is not unique within user returns none, error code and message.
        """
        account, code, message = Account.get(account_id)
        if not account:  # No such account
            return account, code, message

        if not name and user_id == -1:
            # Nothing to do
            return None, 400, "Name or user id required"

        if not name:
            name = account.name

        if user_id != -1:
            user, code, message = User.get(user_id)
            if not user:  # No such user
                return user, 412, message
        else:
            user = account.user

        if models.Account.query.filter_by(name=name, user=user).first():
            return None, 409, "Account name must be unique within user"

        account.name = name
        account.user = user
        result, code, message = commit(models.db.session)
        if result:
            return account, 200, "Account updated"
        return None, code, message

    @staticmethod
    def delete(account_id):
        """
        Deletes account object with given account id
        :param int account_id: Id of the account as integer.
        :return: Returns True, success code and message if object is deleted.
            Otherwise returns False, error code and message.
        """
        account, code, message = Account.get(account_id)
        if not account:  # No such account
            return False, code, message
        session = models.db.session
        session.delete(account)
        result, code, message = commit(session)
        if result:
            return True, 200, "OK"
        return False, code, message


class Admin:
    @staticmethod
    def get(admin_id=1):
        """
        Get admin object with given admin id
        :param int admin_id: Id of the account as integer.
        :return: If admin id is found returns the admin object, OK code and message.
            Otherwise returns none, error code and message.
        """
        admin = models.Admin.query.get(admin_id)
        if admin:
            return admin, 200, "OK"
        return None, 404, "No such admin"

    @staticmethod
    def get_all():
        """
        Get all admin objects as list.
        :return: returns list of all admin objects, OK code and message.
        """
        return models.Admin.query.all(), 200, "OK"

    @staticmethod
    def create(user_id, password):
        """
        Creates admin object with given password for given user id.
        :param int user_id: Id of the user of admin object as integer.
        :param str password: Password for the admin as string. Must be at least 8 characters long.
        :return: If user id exists and user is not already admin and password is valid returns new admin object, success
            code and message. Otherwise returns none, error code and message.
        """
        user, code, message = User.get(user_id)
        if not user:  # No such user
            return user, 412, message

        if len(password) < 8:
            return None, 400, "Password is too short"

        admin = models.Admin(user, password)
        session = models.db.session
        session.add(admin)
        result, code, message = commit(session)
        if result:
            return admin, 201, "Admin created"
        return None, code, message

    @staticmethod
    def edit(admin_id, password):
        """
        Edits admin password for given id.
        :param int admin_id: Id of the admin as integer.
        :param str password: New password for admin. Needs to be at least 8 characters long.
        :return: Returns edited admin object, success code and message if id exists and password is valid.
            Otherwise returns none, error code and message.
        """

        admin, code, message = Admin.get(admin_id)
        if not admin:  # No such admin
            return admin, code, message

        if len(password) < 8:
            return None, 400, "Password is too short"

        admin.password_hash = models.Admin.hash_password(password)
        result, code, message = commit(models.db.session)
        if result:
            return admin, 200, "Admin updated"
        return None, code, message

    @staticmethod
    def delete(admin_id):
        """
        Deletes admin object with given account id
        :param int admin_id: Id of the admin as integer.
        :return: Returns True, success code and message if object is deleted.
            Otherwise returns False, error code and message.
        """
        admin, code, message = Admin.get(admin_id)
        if not admin:  # No such admin
            return False, code, message
        session = models.db.session
        session.delete(admin)
        result, code, message = commit(session)
        if result:
            return True, 200, "Admin deleted"
        return False, code, message


class Card:
    @staticmethod
    def get(card_id=1, sha=""):
        """
        Get card object with given card id or SHA
        :param int card_id: Id of the card as integer. Default is 1.
        :param str sha: SHA of the card as a string. Default is empty string. If this is set then
        search by this instead of id.
        :return: If card id is found returns the card object, OK code and message.
            Otherwise returns none, error code and message.
        """
        if sha:
            card = models.Card.query.filter_by(sha=sha).first()
        else:
            card = models.Card.query.get(card_id)
        if card:
            return card, 200, "OK"
        return None, 404, "No such card"

    @staticmethod
    def get_all():
        """
        Get all card objects as list.
        :return: returns list of all card objects, OK code and message.
        """
        return models.Card.query.all(), 200, "OK"

    @staticmethod
    def get_unassigned():
        """
        Get all unassigned card objects as list.
        :return: list of all card objects, OK code and message.
        """
        return models.Card.query.filter_by(account_id=None).all(), 200, "OK"

    @staticmethod
    def create(name, sha, account_id=0):
        """
        Creates card object with given name and sha for account_id.
        :param str name: Name of the account. Must be unique within account.
        :param str sha: sha256 hash from the physical card.
        :param int account_id: Id of the account of the card.
        :return: If account id is valid and name is unique within account returns new card object, success code and
            message. Otherwise returns none, error code and message.
        """
        if not sha:
            # Name and SHA are required
            return None, 400, "SHA required"

        if len(sha) < 64:
            # Too short hash
            return None, 400, "SHA is too short"

        if name is None:
            name = sha[:64]
        elif not name:  # Check against empty strings
            return None, 400, "Name can't be empty"

        if account_id:
            account, code, message = Account.get(account_id)
            if not account:  # No such account
                return account, 412, message

            if models.Card.query.filter_by(name=name, account=account).first():
                return None, 409, "Card name must be unique within account"
        else:
            account = None

        card = models.Card(name, sha, account)
        session = models.db.session
        session.add(card)
        result, code, message = commit(session)
        if result:
            return card, 201, "Card created"
        return None, code, message

    @staticmethod
    def edit(card_id, name="", account_id=-1):
        """
        Edits card with given id. If name and/or account id is given it will become new name/account id. If name and or
        account id is not given: they will remain the same.
        :param int card_id: Id of the card as integer.
        :param str name: New name of the card as string. Must be unique within user.
        :param int account_id: New account of the card as string. Account must not have card with same name.
        :return: If name for card is unique returns edited card object, success code and message.
            if object is not edited or name is not unique within account returns none, error code and message.
        """
        card, code, message = Card.get(card_id)
        if not card:  # No such card
            return card, code, message

        if not name and account_id == -1:
            return None, 400, "Name or account id required"

        if not name:
            name = card.name

        if not account_id:
            account = None
        elif account_id == -1:
            account = card.account
        else:
            account, code, message = Account.get(account_id)
            if not account:  # No such account
                return account, 412, message

        if models.Card.query.filter_by(name=name, account=account).first():
            return None, 409, "Card name must be unique within user"

        card.name = name
        card.account = account
        result, code, message = commit(models.db.session)
        if result:
            return card, 200, "Card updated"
        return None, code, message

    @staticmethod
    def delete(card_id):
        """
        Deletes card object with given card id
        :param int card_id: Id of the card as integer.
        :return: Returns True, success code and message if object is deleted.
            Otherwise returns False, error code and message.
        """
        card, code, message = Card.get(card_id)
        if not card:  # No such card
            return False, code, message
        session = models.db.session
        session.delete(card)
        result, code, message = commit(session)
        if result:
            return True, 200, "Card deleted"
        return False, code, message


class Register:
    @staticmethod
    def get(register_id=1, sha=""):
        """
        Get register object with given register id or SHA
        :param int register_id: Id of the register as integer.
        :param str sha: SHA of the register as a string. Default is empty string. If this is set
        then search by this instead of id.
        :return: If register id is found returns the register object, OK code and message.
            Otherwise returns none, error code and message.
        """
        if sha:
            register = models.Register.query.filter_by(sha=sha).first()
        else:
            register = models.Register.query.get(register_id)
        if register:
            return register, 200, "OK"
        return None, 404, "No such register"

    @staticmethod
    def get_all():
        """
        Get all register objects as list.
        :return: returns list of all register objects, OK code and message.
        """
        return models.Register.query.all(), 200, "OK"

    @staticmethod
    def create(name, sha, register_type=0):
        """
        Creates register object with given name and sha and register type.
        :param str name: Name of the account. Must be unique.
        :param str sha: sha256 hash from the physical register.
        :param int register_type: Type of the register.
            (0 = slave. only for money withdraw. 1 = master. editing enabled)
        :return: If name is is unique returns new register object, success code and message. Otherwise returns none,
            error code and message.
        """
        if not name:
            return None, 400, "Name must not be empty"
        if register_type not in [0, 1]:
            return None, 400, "Invalid register type"

        if len(sha) < 64:
            return None, 400, "SHA is too short"

        register = models.Register(name, sha, register_type)
        session = models.db.session
        session.add(register)
        result, code, message = commit(session)
        if result:
            return register, 201, "Register created"
        return None, code, message

    @staticmethod
    def edit(register_id, name="", register_type=None):
        """
        Edits register with given id. If name and/or register type is given it will become new name/type. If name and or
        register type is not given: they will remain the same.
        :param int register_id: Id of the register as integer.
        :param str name: New name of the register as string. Must be unique.
        :param int register_type: New type of the register type. .
        :return: Returns edited register if name for register is unique and type is valid.
            If register name or type is not edited; returns none.

        :return: If name for register is unique and type is valid returns edited account object, success code and
            message. If register name or type is not edited; returns none, error code and message.
        """
        register, code, message = Register.get(register_id)
        if not register:  # No such register
            return register, code, message

        if not name and register_type is None:
            return None, 400, "Name or register type required"

        if not name:
            name = register.name

        if register_type is not None:
            if register_type not in [0, 1]:
                return None, 400, "Invalid register type"

        register.name = name
        register.type = register_type
        result, code, message = commit(models.db.session)
        if result:
            return register, 200, "Register updated"
        return None, code, message

    @staticmethod
    def delete(register_id):
        """
        Deletes register object with given register id
        :param int register_id: Id of the register as integer.
        :return: Returns True, success code and message if object is deleted.
            Otherwise returns False, error code and message.
        """
        register, code, message = Register.get(register_id)
        if not register:
            return False, code, message
        session = models.db.session
        session.delete(register)
        result, code, message = commit(session)
        if result:
            return True, 200, "Register deleted"
        return False, code, message


class Transaction:
    @staticmethod
    def get(transaction_id=1):
        """
        Get transaction object with given transaction id
        :param int transaction_id: Id of the register as integer.
        :return: If transaction id is found returns the transaction object, OK code and message.
            Otherwise returns none, error code and message.
        """
        transaction = models.Transaction.query.get(transaction_id)
        if transaction:
            return transaction, 200, "OK"
        return None, 404, "No such transaction"

    @staticmethod
    def get_all(page=0):
        """
        Get all transaction objects as list.
        :return: returns list of all transaction objects, OK code and message.
        """
        if not page:
            return models.Transaction.query.all(), 200, "OK"
        return models.Transaction.query.paginate(page, 20), 200, "OK"

    @staticmethod
    def get_by_account(account_id, page=0):
        if not page:
            return models.Transaction.query.filter_by(account_id=account_id).all(), 200, "OK"
        return models.Transaction.query.filter_by(account_id=account_id).paginate(page, 20), 200, "OK"

    @staticmethod
    def get_by_card(card_id, page=0):
        if not page:
            return models.Transaction.query.filter_by(card_id=card_id).all(), 200, "OK"
        return models.Transaction.query.filter_by(card_id=card_id).paginate(page, 20), 200, "OK"

    @staticmethod
    def get_by_register(register_id, page=0):
        if not page:
            return models.Transaction.query.filter_by(register_id=register_id).all(), 200, "OK"
        return models.Transaction.query.filter_by(register_id=register_id).paginate(page, 20), 200, "OK"

    @staticmethod
    def get_by_user(user_id, page=0):
        if not page:
            return models.Transaction.query.filter_by(user_id=user_id).all(), 200, "OK"
        return models.Transaction.query.filter_by(user_id=user_id).paginate(page, 20), 200, "OK"

    @staticmethod
    def create(card_id, register_id, balance_change):
        """
        Creates transaction object with given card id, register id and balance_change.
        :param int card_id: Id of the card.
        :param int register_id: Id of the register.
        :param float balance_change: Amount of balance changed in transaction.
        :return: if card and register ids are valid checks if card has enough balance: if so returns transaction object,
            success code and message. If anything fails returns None, correct error code and message.
        """
        card, code, message = Card.get(card_id)
        if not card:  # No such card
            return card, 412, message

        if not card.account:
            return None, 412, "Cannot create transaction on unassigned cards"

        register, code, message = Register.get(register_id)
        if not register:  # No such register
            return register, 412, message

        if register.type != 1 and balance_change >= 0:
            return None, 412, "Cannot add funds on regular registers"

        if abs(balance_change) >= maxsize:
            return None, 400, "Invalid balance change value"
        if balance_change < 0 and card.account.balance() + balance_change < 0:
            return None, 412, "Insufficient funds"

        transaction = models.Transaction(card.account.user, card.account, card, register, balance_change)
        session = models.db.session
        session.add(transaction)
        result, code, message = commit(session)
        if result:
            return transaction, 201, "Transaction created"
        return None, code, message

    @staticmethod
    def delete(transaction_id):
        """
        Deletes transaction object with given transaction id
        :param int transaction_id: Id of the transaction as integer.
        :return: Returns True, success code and message if object is deleted.
            Otherwise returns False, error code and message.
        """
        transaction, code, message = Transaction.get(transaction_id)
        if not transaction:  # No such transaction
            return False, code, message
        session = models.db.session
        session.delete(transaction)
        result, code, message = commit(session)
        if result:
            return True, 200, "Transaction deleted"
        return False, code, message


class User:
    @staticmethod
    def get(user_id=1):
        """
        Get user object with given user id
        :param int user_id: Id of the user as integer.
        :return: If user id is found returns the user object, OK code and message.
            Otherwise returns none, error code and message.
        """
        user = models.User.query.get(user_id)
        if user:
            return user, 200, "OK"
        return None, 404, "No such user"

    @staticmethod
    def get_all():
        """
        Get all user objects as list.
        :return: returns list of all user objects, OK code and message.
        """
        return models.User.query.all(), 200, "OK"

    @staticmethod
    def create(name, email, phone=""):
        """
        Creates user object with given name, email and phone number.
        :param str name: Name of the user.
        :param str email: email of the user as string.
        :param str phone: phone number of the user as string.
        :return: If user information is valid returns new user object, success code and message. Otherwise returns none,
            error code and message.
        """
        name = name.strip()
        email = email.strip()
        if not all((field for field in (name, email))):
            return None, 400, "Name and email required"
        user = models.User(name, email, phone)
        session = models.db.session
        session.add(user)
        result, code, message = commit(session)
        if result:
            return user, 201, "User created"
        return None, code, message

    @staticmethod
    def edit(user_id, name=None, email=None, phone=None):
        """
        Edits user with given id. If name, email and/or phone number is given it will become new name/type. If name,
        email and/or phone number is not given: they will remain the same.
        :param int user_id: Id of the user as integer.
        :param str name: New name of the user as string.
        :param str email: New email of the user as string.
        :param str phone: New phone number of the user as string.
        :return: Returns edited user, success code and message if new attributes are given.
            If user name, email and phone number is not edited; returns none, error code and message.
        """
        user, code, message = User.get(user_id)
        if not user:  # No such user
            return user, code, message

        if name is None and email is None and phone is None:
            return None, 400, "Name, email or phone required"

        if name is None:
            name = user.name

        if email is None:
            email = user.email

        if phone is None:
            phone = user.phone

        name = name.strip()
        if not name:
            return None, 400, "Invalid name"
        email = email.strip()
        if not email:
            return None, 400, "Invalid email"

        user.name = name
        user.email = email
        user.phone = phone
        result, code, message = commit(models.db.session)
        if result:
            return user, 200, "User updated"
        return None, code, message

    @staticmethod
    def delete(user_id):
        """
        Deletes user object with given user id
        :param int user_id: Id of the user as integer.
        :return: Returns True, success code and message if object is deleted.
            Otherwise returns False, error code and message.
        """
        user, code, message = User.get(user_id)
        if not user:  # No such user
            return False, code, message
        session = models.db.session
        session.delete(user)
        result, code, message = commit(session)
        if result:
            return True, 200, "User deleted"
        return False, code, message

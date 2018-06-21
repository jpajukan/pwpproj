import os
import sys
import pytest

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../.."))

from db.api import *
from init_db import *

main()

application = init_app()
init_db(application.app)


#Account


existingaccountname = "Ruokatili"
existingaccountid = 1
existingaccountuserid = 1
existinguserid = 1
numberofallaccounts = 5

duplicateaccountname = "Viinatili"

nonexistingaccountid = 1234567
nonexistinguserid = 123456

accountname = "Veronkiertoaccountti"


def test_account_get():
    """
    Test getting account by id
    """
    a, code, message = Account.get(existingaccountid)
    assert code == 200
    assert a.name == existingaccountname
    assert message == "OK"


def test_account_get_account_not_exist():
    """
    Try getting nonexistent account
    """
    a, code, message = Account.get(nonexistingaccountid)
    assert a is None
    assert code == 404
    assert message == "No such account"


def test_account_get_all():
    """
    Test getting all accounts
    """
    a, code, message = Account.get_all()
    numberofaccounts = len(a)
    assert numberofaccounts == numberofallaccounts
    assert code == 200
    assert message == "OK"


def test_account_create_user_not_exist():
    """
    Try creating account for user that does not exist
    """
    a, code, message = Account.create("Testaccount", nonexistinguserid)
    assert a is None
    assert code == 412
    assert message == "No such user"


def test_account_create_duplicate_account_name():
    """
    Try creating account with duplicate name
    """
    a, code, message = Account.create(existingaccountname, existinguserid)
    assert a is None
    assert code == 409
    assert message == "Name must be unique within user"

def test_account_create_empty_account_name():
    """
    Try creating account with empty name
    """
    a, code, message = Account.create("", existinguserid)
    assert a is None
    assert code == 400
    assert message == "Name must not be empty"


def test_account_create():
    """
    Test account creation
    """
    a, code, message = Account.create(accountname, 1)

    assert a is not None
    assert a.name == accountname
    assert a.user.id == 1
    assert code == 201
    assert message == "Account created"


def test_account_delete():
    """
    Test account deletion
    """
    a, code, message = Account.delete(6)

    assert a is True
    assert code == 200
    assert message == "OK"

    a2, code2, message2 = Account.get(6)
    assert a2 is None
    assert code2 == 404


def test_account_delete_account_not_exist():
    """
    Try deleting nonexistent account
    """
    a, code, message = Account.delete(nonexistingaccountid)
    assert a is False
    assert code == 404
    assert message == "No such account"


def test_account_edit_account_not_exist():
    """
    Try editing nonexistent account
    """
    a, code, message = Account.edit(nonexistingaccountid, "newname1234567", 0)
    assert a is None
    assert code == 404
    assert message == "No such account"


def test_account_edit_account_name_already_exists():
    """
    Try editing account to have same name that another account within a user
    """
    checkitembefore, code, message = Account.get(1)
    checkitembeforedump = checkitembefore.dump()

    a, code, message = Account.edit(existingaccountid, duplicateaccountname)
    assert a is None
    assert code == 409
    assert message == "Account name must be unique within user"

    checkitemafter, code, message = Account.get(1)

    assert checkitembeforedump == checkitemafter.dump()


def test_account_edit_given_user_not_exist():
    """
    Try assign account to nonexistent user
    """
    checkitembefore, code, message = Account.get(1)
    checkitembeforedump = checkitembefore.dump()

    a, code, message = Account.edit(existingaccountid, "namething54321", nonexistinguserid)
    assert a is None
    assert code == 412
    assert message == "No such user"

    checkitemafter, code, message = Account.get(1)

    assert checkitembeforedump == checkitemafter.dump()


def test_account_balance():
    """
    Test getting account balances
    """
    a, code, message = Account.get(1)

    assert a is not None
    assert code == 200
    assert a.balance() == 0
    assert message == "OK"

    a2, code2, message2 = Account.get(5)

    assert a2 is not None
    assert code2 == 200
    assert a2.balance() == 6.7



#Admin


existingadminuserid = 6


def test_admin_get():
    """
    Test getting admin by id
    """
    a, code, message = Admin.get(1)
    assert a is not None
    assert code == 200
    assert message == "OK"


def test_admin_get_admin_not_exist():
    """
    Try get nonexistent admin
    """
    a, code, message = Admin.get(123456)
    assert a is None
    assert code == 404
    assert message == "No such admin"


def test_admin_get_all():
    """
    Test getting all admins
    """
    a, code, message = Admin.get_all()
    numberofaccounts = len(a)
    assert numberofaccounts == 1
    assert code == 200
    assert message == "OK"


def test_admin_create():
    """
    Test creating new admin
    """
    adminuserid = 1
    validpassword = "nicegoodpassword"

    a, code, message = Admin.create(adminuserid, validpassword)

    assert a is not None
    assert a.user.id == adminuserid
    assert code == 201
    assert message == "Admin created"


def test_admin_create_user_not_exist():
    """
    Try giving admin rights to nonexistent user
    """
    a, code, message = Admin.create(1234565, "passorddddddd")
    assert a is None
    assert code == 412
    assert message == "No such user"


def test_admin_create_empty_password():
    """
    Try creating admin with empty password
    """
    a, code, message = Admin.create(1, "")
    assert a is None
    assert code == 400
    assert message == "Password is too short"


def test_admin_create_short_password():
    """
    Try creating admin with invalid password
    """
    a, code, message = Admin.create(1, "aaaa")
    assert a is None
    assert code == 400
    assert message == "Password is too short"


def test_admin_create_user_is_already_admin():
    """
    Try give admin rights to user which is already admin
    """
    a, code, message = Admin.create(existingadminuserid, "validpassword")
    assert a is None
    assert code == 409
    assert message == "Integrity constraint failed"


def test_admin_edit_admin_not_exist():
    """
    Try editing nonexistent admin
    """
    a, code, message = Admin.edit(12345678, "passowrkss")
    assert a is None
    assert code == 404
    assert message == "No such admin"


def test_admin_edit_empty_password():
    """
    Try editing admin to have empty password
    """
    a, code, message = Admin.edit(1, "")
    assert a is None
    assert code == 400
    assert message == "Password is too short"


def test_admin_edit_short_password():
    """
    Try editing admin to have invalid password
    """
    a, code, message = Admin.edit(1, "aaaa")
    assert a is None
    assert code == 400
    assert message == "Password is too short"


def test_admin_edit():
    """
    Test editing admin
    """
    a, code, message = Admin.edit(2, "newvalidpassowrd")
    assert a is not None
    assert code == 200
    assert message == "Admin updated"


def test_admin_delete():
    """
    Test deleting admin
    """
    a, code, message = Admin.delete(2)

    assert a is True
    assert code == 200
    assert message == "Admin deleted"

    a2, code2, message2 = Admin.get(2)
    assert a2 is None
    assert code2 == 404


def test_admin_delete_admin_not_exist():
    """
    Try deleting nonexistent admin
    """
    a, code, message = Admin.delete(123456)
    assert a is False
    assert code == 404
    assert message == "No such admin"


#Cards

shatesthash = "8e869683e0e40211a37bf3ac721c3c3b269fb10cf853255d11b104759526ab9c"
shatesthash2 = "8e869683e0e40211a37bf3ac721c3c3b269fb10cf812555d11b104759526ab9c"



def test_card_get():
    """
    Test getting card by id
    """
    a, code, message = Card.get(1)
    assert a is not None
    assert code == 200
    assert message == "OK"


def test_card_get_by_sha():
    """
    Test getting card by sha
    """
    existingcardhash = "034f5e8d6d75496524c5947923874ed55715989cf4c36b539622085049500336"
    a, code, message = Card.get(sha=existingcardhash)
    assert a is not None
    assert a.name == "Opiskelijakortti"
    assert code == 200
    assert message == "OK"


def test_card_get_by_sha_card_not_exist():
    """
    Test getting nonexistent card by sha
    """
    a, code, message = Card.get(sha=shatesthash)
    assert a is None
    assert code == 404
    assert message == "No such card"


def test_card_get_card_not_exist():
    """
    Test getting nonexistent card by id
    """
    a, code, message = Card.get(1234567)
    assert a is None
    assert code == 404
    assert message == "No such card"


def test_card_get_all():
    """
    Test getting all cards
    """
    a, code, message = Card.get_all()
    numberofcards = len(a)
    assert numberofcards == 7
    assert code == 200
    assert message == "OK"


def test_card_create():
    """
    Test creating card
    """
    cardname = "newtestcardname"
    a, code, message = Card.create(cardname, shatesthash2, 1)

    assert a is not None
    assert code == 201
    assert a.name == cardname
    assert a.account.id == 1
    assert message == "Card created"


def test_card_create_empty_name():
    """
    Try creating card with empty name
    """
    a, code, message = Card.create("", shatesthash, 1)
    assert a is None
    assert code == 400
    assert message == "Name can't be empty"


def test_card_create_empty_sha():
    """
    Try creating card with empty sha
    """
    a, code, message = Card.create("validname", "", 1)
    assert a is None
    assert code == 400
    assert message == "SHA required"


def test_card_create_duplicate_name():
    """
    Try creating card with duplicate name within user
    """
    a, code, message = Card.create("Opiskelijakortti", shatesthash, 1)
    assert a is None
    assert code == 409
    assert message == "Card name must be unique within account"


def test_card_create_duplicate_sha():
    """
    Try creating card with existing sha
    """
    a, code, message = Card.get(1)
    assert a is not None
    assert code == 200

    a2, code2, message2 = Card.create("validnameforcard", a.sha, 1)
    assert a2 is None
    assert code2 == 409
    assert message2 == "Integrity constraint failed"


def test_card_create_invalid_sha():
    """
    Try creating card with invalid (too short) sha
    """
    a, code, message = Card.create("validname4567", "invalidsha", 1)
    assert a is None
    assert code == 400
    assert message == "SHA is too short"


def test_card_edit_card_not_exist():
    """
    Try editing nonexistent card
    """
    a, code, message = Card.edit(123456, "validname8654", 1)
    assert a is None
    assert code == 404
    assert message == "No such card"


def test_card_edit_duplicate_name():
    """
    Try edit card to have duplicate name within user
    """
    checkitembefore, code, message = Card.get(1)
    checkitembeforedump = checkitembefore.dump()

    a, code, message = Card.edit(1, "Kännykkä", 1)
    assert a is None
    assert code == 409
    assert message == "Card name must be unique within user"

    checkitemafter, code, message = Card.get(1)

    assert checkitembeforedump == checkitemafter.dump()


def test_card_edit_account_not_exist():
    """
    Try assign card to nonexistent account
    """
    checkitembefore, code, message = Card.get(1)
    checkitembeforedump = checkitembefore.dump()

    a, code, message = Card.edit(1, "renamevalidname", 123456)
    assert a is None
    assert code == 412
    assert message == "No such account"

    checkitemafter, code, message = Card.get(1)

    assert checkitembeforedump == checkitemafter.dump()


def test_card_delete():
    """
    Test card delete
    """
    a, code, message = Card.delete(8)

    assert a is True
    assert code == 200
    assert message == "Card deleted"

    a2, code2, message2 = Card.get(8)
    assert a2 is None
    assert code2 == 404


def test_card_delete_card_not_exist():
    """
    Try delete nonexistent card
    """
    a, code, message = Card.delete(123456)
    assert a is False
    assert code == 404
    assert message == "No such card"


#Register
numberofallregisters = 3
shatesthashforregister = "998A364B79915F8C78D2646F885217EF1B0E30994D2E376439EC0741B366E331"
duplicateregistername = "Admin"

registerid2sha =  "d0e126c321575bf2b42f45755e1fb1525219d22d03b4baa4c81fbdd8bca3cdef"


def test_register_get():
    """
    Test getting register by id
    """
    a, code, message = Register.get(1)
    assert a is not None
    assert code == 200
    assert message == "OK"


def test_register_get_register_not_exist():
    """
    Try getting nonexistent register
    """
    a, code, message = Register.get(1234567)
    assert a is None
    assert code == 404
    assert message == "No such register"


def test_register_get_by_sha():
    """
    Test getting register by sha
    """
    a, code, message = Register.get(sha=registerid2sha)
    assert a is not None
    assert code == 200
    assert message == "OK"


def test_register_get_by_sha_register_not_exist():
    """
    Try getting nonexistent register
    """
    a, code, message = Register.get(sha=shatesthashforregister)
    assert a is None
    assert code == 404
    assert message == "No such register"


def test_register_get_all():
    """
    Test getting all registers
    """
    a, code, message = Register.get_all()
    assert a is not None
    assert code == 200
    assert len(a) == 3
    assert message == "OK"


def test_register_create():
    """
    Test creating register
    """
    newregistername = "newsupercoolregister"
    sha = "998A364B79915F8C78D2646F885217EF1B0E30994D2E376439EC0741B366E666"
    a, code, message = Register.create(newregistername, sha, 0)
    assert a is not None
    assert code == 201
    assert a.name == newregistername
    assert message == "Register created"


def test_register_create_empty_name():
    """
    Try creating register with empty name
    """
    a, code, message = Register.create("", shatesthashforregister, 0)
    assert a is None
    assert code == 400
    assert message == "Name must not be empty"


def test_register_create_duplicate_name():
    """
    Test getting account by id
    """
    a, code, message = Register.create(duplicateregistername, shatesthashforregister, 0)
    assert a is None
    assert code == 409
    assert message == "Integrity constraint failed"


def test_register_create_empty_sha():
    """
    Try create register with empty sha
    """
    a, code, message = Register.create("newregistername", "", 0)
    assert a is None
    assert code == 400
    assert message == "SHA is too short"


def test_register_create_invalid_sha():
    """
    Try creating register with invalid (too short) sha
    """
    a, code, message = Register.create("registername", "invalidshafdfgfsfgfd", 0)
    assert a is None
    assert code == 400
    assert message == "SHA is too short"


def test_register_create_invalid_type():
    """
    Try creating register with invalid type
    """
    a, code, message = Register.create("registername", shatesthashforregister, 5000)
    assert a is None
    assert code == 400
    assert message == "Invalid register type"


def test_register_edit():
    """
    Test editing register
    """
    checkitembefore, code, message = Register.get(4)
    checkitembeforedump = checkitembefore.dump()

    registernewvalidname = "supervalidnewname"
    a, code, message = Register.edit(4, registernewvalidname, 1)
    assert a is not None
    assert code == 200
    assert a.name == registernewvalidname
    assert a.type == 1
    assert message == "Register updated"

    checkitemafter, code, message = Register.get(4)

    assert checkitembeforedump != checkitemafter.dump()


def test_register_edit_register_not_exist():
    """
    Try editing nonexistent register
    """
    a, code, message = Register.edit(123456, "validnewname", 0)
    assert a is None
    assert code == 404
    assert message == "No such register"


def test_register_edit_duplicate_name():
    """
    Try editing register to have duplicate name
    """
    checkitembefore, code, message = Register.get(1)
    checkitembeforedump = checkitembefore.dump()

    a, code, message = Register.edit(1, duplicateregistername)
    assert a is None
    assert code == 409
    assert message == "Integrity constraint failed"

    checkitemafter, code, message = Register.get(1)

    assert checkitembeforedump == checkitemafter.dump()


def test_register_edit_invalid_type():
    """
    Try editing register to have invalid type
    """
    checkitembefore, code, message = Register.get(1)
    checkitembeforedump = checkitembefore.dump()

    a, code, message = Register.edit(1, "Somenewnamenolol1", 50000)
    assert a is None
    assert code == 400
    assert message == "Invalid register type"

    checkitemafter, code, message = Register.get(1)

    assert checkitembeforedump == checkitemafter.dump()


def test_register_delete():
    """
    Test deleting register
    """
    a, code, message = Register.delete(4)
    assert a is True
    assert code == 200
    assert message == "Register deleted"

    a2, code2, message2 = Register.get(4)
    assert a2 is None
    assert code2 == 404


def test_register_delete_register_not_exist():
    """
    Try deleting nonexistent register
    """
    a, code, message = Register.delete(123456)
    assert a is False
    assert code == 404
    assert message == "No such register"


# Transactions

numberofalltransactions = 16


def test_transaction_get():
    """
    Test getting transaction by id
    """
    a, code, message = Transaction.get(1)
    assert a is not None
    assert code == 200
    assert message == "OK"


def test_transaction_get_transaction_not_exist():
    """
    Try getting nonexistent transaction
    """
    a, code, message = Transaction.get(1234567)
    assert a is None
    assert code == 404
    assert message == "No such transaction"


def test_transaction_get_all():
    """
    Test getting all transactions
    """
    a, code, message = Transaction.get_all()

    assert len(a) == numberofalltransactions
    assert code == 200
    assert message == "OK"


def test_transaction_create():
    """
    Test creating transaction
    """
    a, code, message = Transaction.create(6, 1, -1)

    assert a is not None
    assert code == 201
    assert message == "Transaction created"


def test_transaction_create_card_not_exist():
    """
    Try crating transaction with nonexistent card
    """
    a, code, message = Transaction.create(123456, 1, -1)
    assert a is None
    assert code == 412
    assert message == "No such card"


def test_transaction_create_register_not_exist():
    """
    Try creating transaction with nonexistent register
    """
    a, code, message = Transaction.create(1, 123456, -1)
    assert a is None
    assert code == 412
    assert message == "No such register"


def test_transaction_create_negative_balance_result():
    """
    Try draw more funds than the account haves on it
    """
    a, code, message = Transaction.create(1, 1, -1234)
    assert a is None
    assert code == 412
    assert message == "Insufficient funds"


def test_transaction_create_card_unassigned():
    """
    Try create transaction with card that has not been assigned to any account
    """
    a, code, message = Transaction.create(7, 1, -1)
    assert a is None
    assert code == 412
    assert message == "Cannot create transaction on unassigned cards"


def test_transaction_create_register_not_admin_for_money_insert():
    """
    Try insert money to account without using tha admin register
    """
    a, code, message = Transaction.create(1, 1, 1)
    assert a is None
    assert code == 412
    assert message == "Cannot add funds on regular registers"


def test_transaction_delete():
    """
    Test deleting transaction
    """
    a, code, message = Transaction.delete(17)
    assert a is True
    assert code == 200
    assert message == "Transaction deleted"

    a2, code2, message2 = Transaction.get(17)
    assert a2 is None
    assert code2 == 404


def test_transaction_delete_transaction_not_exist():
    """
    Try deleting nonexistent transaction
    """
    a, code, message = Transaction.delete(123456)
    assert a is False
    assert code == 404
    assert message == "No such transaction"


# User

numberofallusers = 6

newuserphone = "0402469218"
newuseremail = "kkkdddsssaa@gmail.com"

newuserinvalidname = "klafsdlkjasfdlkjaslkfdjalskjfdlkasjdflkjaslkdfjaslkfdjlksajfdlkajsdlkfjaslkdfjlkj alsdkfjalksd fjlkasjdf lksajdlfkj fsdjlkasdfj l"
newuserinvalidemail = "dskfjalksdjflkajsdf lkasdjf lkasjfd lkasjdfkas fjlkasj dflksaj dflkjas fdlkj aslkfj askldf lksa fdjlksadjfj"

newuserinvalidphone = "6756765756756765756 56 56756756 65 5675 67 567 56  765 7567567657 576 56 765 7567 56765 657657 567 657 7 567567"

newuserduplicateemail = "toukopouko@example.com"


def test_user_get():
    """
    Test getting user by id
    """
    a, code, message = User.get(1)
    assert a is not None
    assert code == 200
    assert message == "OK"


def test_user_get_user_not_exist():
    """
    Try getting nonexistent user
    """
    a, code, message = User.get(1234567)
    assert a is None
    assert code == 404
    assert message == "No such user"


def test_user_get_all():
    """
    Test getting all users
    """
    a, code, message = User.get_all()
    assert len(a) == numberofallusers
    assert code == 200
    assert message == "OK"


def test_user_create():
    """
    Test creating user
    """
    name = "coolusername"
    email = "cool@mail.com"
    phone = "0406548296"

    a, code, message = User.create(name, email, phone)

    assert a is not None
    assert code == 201
    assert a.name == name
    assert a.email == email
    assert a.phone == phone
    assert message == "User created"


def test_user_create_empty_name():
    """
    Try creating user with empty name
    """
    a, code, message = User.create("", newuseremail, newuserphone)
    assert a is None
    assert code == 400
    assert message == "Name and email required"


def test_user_create_name_invalid():
    """
    Try creating user with invalid (too long) name
    """
    a, code, message = User.create(newuserinvalidname, newuseremail, newuserphone)
    assert a is None
    assert code == 400
    assert message == "Data constraint failed"


def test_user_create_email_invalid():
    """
    Try creating user with invalid (too long) email
    """
    a, code, message = User.create("newusername", newuserinvalidemail, newuserphone)
    assert a is None
    assert code == 400
    assert message == "Data constraint failed"


def test_user_create_phone_invalid():
    """
    Try creating user with invalid (too long) phone number
    """
    a, code, message = User.create("namenewuser", newuseremail, newuserinvalidphone)
    assert a is None
    assert code == 400
    assert message == "Data constraint failed"


def test_user_edit():
    """
    Test editing user
    """
    name = "coolusernamet"
    email = "cool@mail.comt"
    phone = "0406548296t"

    checkitembefore, code, message = User.get(7)
    checkitembeforedump = checkitembefore.dump()

    a, code, message = User.edit(7, name, email, phone)

    assert a is not None
    assert code == 200
    assert a.name == name
    assert a.email == email
    assert a.phone == phone
    assert message == "User updated"

    checkitemafter, code, message = User.get(7)

    assert checkitembeforedump != checkitemafter.dump()


def test_user_edit_user_not_exist():
    """
    Test editing nonexistent user
    """
    a, code, message = User.edit(123456, "name", "email", "phone")
    assert a is None
    assert code == 404
    assert message == "No such user"


def test_user_edit_user_email_duplicate():
    """
    Try editing user with invalid (duplicate) email
    """
    checkitembefore, code, message = User.get(1)
    checkitembeforedump = checkitembefore.dump()

    a, code, message = User.edit(1, "name", newuserduplicateemail, newuserphone)
    assert a is None
    assert code == 409
    assert message == "Integrity constraint failed"

    checkitemafter, code, message = User.get(1)

    assert checkitembeforedump == checkitemafter.dump()


def test_user_edit_user_name_invalid():
    """
    Try editing user with invalid (too long) name
    """
    checkitembefore, code, message = User.get(1)
    checkitembeforedump = checkitembefore.dump()

    a, code, message = User.edit(1, name=newuserinvalidname)
    assert a is None
    assert code == 400
    assert message == "Data constraint failed"

    checkitemafter, code, message = User.get(1)

    assert checkitembeforedump == checkitemafter.dump()


def test_user_edit_user_email_invalid():
    """
    Try editing user with invalid (too long) email
    """
    checkitembefore, code, message = User.get(1)
    checkitembeforedump = checkitembefore.dump()

    a, code, message = User.edit(1, email=newuserinvalidemail)
    assert a is None
    assert code == 400
    assert message == "Data constraint failed"

    checkitemafter, code, message = User.get(1)

    assert checkitembeforedump == checkitemafter.dump()


def test_user_edit_user_phone_invalid():
    """
    Try editing user with invalid (too long) phone
    """
    checkitembefore, code, message = User.get(1)
    checkitembeforedump = checkitembefore.dump()

    a, code, message = User.edit(1, phone=newuserinvalidphone)
    assert a is None
    assert code == 400
    assert message == "Data constraint failed"

    checkitemafter, code, message = User.get(1)

    assert checkitembeforedump == checkitemafter.dump()


def test_user_delete():
    """
    Test user deletion
    """
    a, code, message = User.delete(7)
    assert a is True
    assert code == 200
    assert message == "User deleted"

    a2, code2, message2 = User.get(7)
    assert a2 is None
    assert code2 == 404


def test_user_delete_user_not_exist():
    """
    Try deleting nonexistent user
    """
    a, code, message = User.delete(123456)
    assert a is False
    assert code == 404
    assert message == "No such user"


# Dumps

def test_account_dump():
    name = "shinynewaccountname"
    userid = 1
    a, code, message = Account.create(name, userid)
    accountid = a.id

    assert a is not None

    expectedresult = {
        "accountId":    accountid,
        "name":         name,
        "userId":       userid
    }

    assert a.dump() == expectedresult


def test_user_dump():
    name = "coolusername55"
    email = "cool@mail.com2"
    phone = "04065482965"

    a, code, message = User.create(name, email, phone)

    assert a is not None

    expectedresult = {
        "name":     name,
        "email":    email,
        "phone":    phone
    }

    assert a.dump() == expectedresult


def test_card_dump():
    sha = "8b940be7fb78aaa6b6567dd7a3987996947460df1c668e698eb92ca77e425349"
    name = "Supercoolnewcard"
    accountid = 1

    a, code, message = Card.create(name, sha, accountid)

    assert a is not None

    expectedresult = {
        "cardId":       sha,
        "name":         name,
        "accountId":    accountid
    }

    assert a.dump() == expectedresult


def test_register_dump():
    name = "newsupercoolregister1337"
    sha = "998A364B79915F8C78D2646F885217EF1B0E30994D2E376439EC0741B366E669"
    rtype = 1

    a, code, message = Register.create(name, sha, rtype)
    assert a is not None

    expectedresult = {
        "registerId":   sha,
        "name":         name,
        "type":         rtype
    }

    assert a.dump() == expectedresult


def test_transaction_dump():

    cardid = 6
    registerid = 1
    balancechange = -1

    userdump = {
        "name":     "Touko Pekkala",
        "email":    "toukopouko@example.com",
        "phone":    None
    }

    accountdump = {
        "accountId":    5,
        "name":         "Salatili",
        "userId":       4
    }

    carddump = {
        "cardId":       "0cbd75f30cfb44dd568f5530c63afca88efa72ef9185fc2b91fcc30724fcc9e9",
        "name":         "Opiskelijakortti",
        "accountId":    5
    }

    registerdump = {
        "registerId":   "acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88",
        "name":         "Kahvihuone",
        "type":         0
    }

    a, code, message = Transaction.create(cardid, registerid, balancechange)

    assert a is not None

    expectedresult = {
        "account":          accountdump,
        "balanceChange":    balancechange,
        "card":             carddump,
        "register":         registerdump,
        "user":             userdump,
        "timestamp":        a.timestamp.isoformat()
    }

    assert a.dump() == expectedresult


def test_admin_generate_and_verify_auth_token():
    """
    Generate authentication token and verify it
    """
    a, code, message = Admin.get(1)
    token = a.generate_auth_token()

    assert len(token) > 64

    a2, code2, message2 = Admin.get(1)
    result = a2.verify_auth_token(token)

    assert result == a


def test_admin_verify_auth_token_invalid():
    """
    Try verification with invalid token
    """
    a2, code2, message2 = Admin.get(1)
    result = a2.verify_auth_token("jafsdölkjasdkfasdfjalskjfdlkasjdflksdlkfjkls")

    assert result is None

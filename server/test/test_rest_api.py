import os
import sys
import json
import pytest
from jsonschema import validate

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../.."))

from init_db import *

main()

application = init_app()
init_db(application.app)

testclient = application.app.test_client()

# TODO: Lisää geteille, posteille ja patcheille testaus validatefunktioissa


# Next 6 functions are for validating admin, user, account, card, register and transaction mason objects

def validate_admin_mason(json_object):
    admin_mason = {
        "type": "object",
        "properties": {
            "@controls": {
                "type": "object",
                "properties": {
                    "cr:create-admin": {
                        "type": "object",
                        "properties": {
                            "encoding": {
                                "type": "string"
                            },
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "schema_url": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["encoding", "href", "method", "schema_url", "title"]
                    },
                    "cr:delete-admin": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["href", "method", "title"]
                    },
                    "cr:edit-admin": {
                        "type": "object",
                        "properties": {
                            "encoding": {
                                "type": "string"
                            },
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "schema_url": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["encoding", "href", "method", "schema_url", "title"]
                    },
                    "self": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            }
                        },
                        "required": ["href"]
                    }
                },
                "required": ["cr:create-admin", "cr:delete-admin", "cr:edit-admin", "self"]
            },
            "admin_id": {
                "type": "number"
            },
            "user": {
                "type": "object",
                "properties": {
                    "@controls": {
                        "type": "object",
                        "self": {
                            "type": "object",
                            "properties": {
                                "href": {
                                    "type": "string"
                                }
                            },
                            "required": ["href"]
                        }
                    },
                    "title": {
                        "type": "string",
                    },
                    "user_id": {
                        "type": "number"
                    }
                },
                "required": ["@controls", "title", "user_id"]
            }
        },
        "required": ["@controls", "admin_id", "user"]
    }

    validate(json_object, admin_mason)


def validate_account_mason(json_object):
    account_mason = {
        "type": "object",
        "properties": {
            "@controls": {
                "type": "object",
                "properties": {
                    "cr:account-transactions": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["href", "method", "title"]
                    },
                    "cr:create-account": {
                        "type": "object",
                        "properties": {
                            "encoding": {
                                "type": "string"
                            },
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "schema_url": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["encoding", "href", "method", "schema_url", "title"]
                    },
                    "cr:delete-account": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["href", "method", "title"]
                    },
                    "cr:edit-account": {
                        "type": "object",
                        "properties": {
                            "encoding": {
                                "type": "string"
                            },
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "schema_url": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["encoding", "href", "method", "schema_url", "title"]
                    },
                    "self": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            }
                        },
                        "required": ["href"]
                    }
                },
                "required": ["cr:account-transactions", "cr:create-account", "cr:delete-account", "cr:edit-account", "self"]
            },
            "account_id": {
                "type": "number"
            },
            "balance": {
                "type": "number"
            },
            "name": {
                "type": "string"
            },
            "cards": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "@controls": {
                            "type": "object",
                            "self": {
                                "type": "object",
                                "properties": {
                                    "href": {
                                        "type": "string"
                                    }
                                },
                                "required": ["href"]
                            }
                        },
                        "card_sha": {
                            "type": "string",
                        },
                        "title": {
                            "type": "string"
                        }

                    }
                }
            },
            "user": {
                "type": "object",
                "properties": {
                    "@controls": {
                        "type": "object",
                        "self": {
                            "type": "object",
                            "properties": {
                                "href": {
                                    "type": "string"
                                }
                            },
                            "required": ["href"]
                        }
                    },
                    "title": {
                        "type": "string",
                    },
                    "user_id": {
                        "type": "number"
                    }
                },
                "required": ["@controls", "title", "user_id"]
            }
        },
        "required": ["@controls", "account_id", "balance", "name", "cards", "user"]
    }

    validate(json_object, account_mason)


def validate_register_mason(json_object):
    register_mason = {
        "type": "object",
        "properties": {
            "@controls": {
                "type": "object",
                "properties": {
                    "cr:register-transactions": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["href", "method", "title"]
                    },
                    "cr:create-register": {
                        "type": "object",
                        "properties": {
                            "encoding": {
                                "type": "string"
                            },
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "schema_url": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["encoding", "href", "method", "schema_url", "title"]
                    },
                    "cr:delete-register": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["href", "method", "title"]
                    },
                    "cr:edit-register": {
                        "type": "object",
                        "properties": {
                            "encoding": {
                                "type": "string"
                            },
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "schema_url": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["encoding", "href", "method", "schema_url", "title"]
                    },
                    "self": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            }
                        },
                        "required": ["href"]
                    }
                },
                "required": ["cr:register-transactions", "cr:create-register", "cr:delete-register", "cr:edit-register", "self"]
            },
            "name": {
                "type": "string"
            },
            "register_sha": {
                "type": "string"
            },
            "type": {
                "type": "number"
            }
        },
        "required": ["@controls", "name", "register_sha", "type"]
    }

    validate(json_object, register_mason)


def validate_user_mason(json_object):
    user_mason = {
        "type": "object",
        "properties": {
            "@controls": {
                "type": "object",
                "properties": {
                    "cr:user-transactions": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["href", "method", "title"]
                    },
                    "cr:create-user": {
                        "type": "object",
                        "properties": {
                            "encoding": {
                                "type": "string"
                            },
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "schema_url": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["encoding", "href", "method", "schema_url", "title"]
                    },
                    "cr:delete-user": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["href", "method", "title"]
                    },
                    "cr:edit-user": {
                        "type": "object",
                        "properties": {
                            "encoding": {
                                "type": "string"
                            },
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "schema_url": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["encoding", "href", "method", "schema_url", "title"]
                    },
                    "self": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            }
                        },
                        "required": ["href"]
                    }
                },
                "required": ["cr:user-transactions", "cr:create-user", "cr:delete-user", "cr:edit-user", "self"]
            },
            "accounts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "@controls": {
                            "type": "object",
                            "self": {
                                "type": "object",
                                "properties": {
                                    "href": {
                                        "type": "string"
                                    }
                                },
                                "required": ["href"]
                            }
                        },
                        "account_id": {
                            "type": "number",
                        },
                        "title": {
                            "type": "string"
                        }

                    }
                }
            },
            "email": {
                "type": "string"
            },
            "name": {
                "type": "string"
            },
            "phone": {
                "type": "string"
            },
            "user_id": {
                "type": "number"
            }
        },
        "required": ["@controls", "accounts", "email", "name", "phone", "user_id"]
    }

    validate(json_object, user_mason)


def validate_card_mason(json_object):
    card_mason = {
        "type": "object",
        "properties": {
            "@controls": {
                "type": "object",
                "properties": {
                    "cr:card-transactions": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["href", "method", "title"]
                    },
                    "cr:create-card": {
                        "type": "object",
                        "properties": {
                            "encoding": {
                                "type": "string"
                            },
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "schema_url": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["encoding", "href", "method", "schema_url", "title"]
                    },
                    "cr:delete-card": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["href", "method", "title"]
                    },
                    "cr:edit-card": {
                        "type": "object",
                        "properties": {
                            "encoding": {
                                "type": "string"
                            },
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "schema_url": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["encoding", "href", "method", "schema_url", "title"]
                    },
                    "self": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            }
                        },
                        "required": ["href"]
                    }
                },
                "required": ["cr:card-transactions", "cr:create-card", "cr:delete-card", "cr:edit-card", "self"]
            },
            "account": {
                "type": "object",
                "properties": {
                    "@controls": {
                        "type": "object",
                        "self": {
                            "type": "object",
                            "properties": {
                                "href": {
                                    "type": "string"
                                }
                            },
                            "required": ["href"]
                        }
                    },
                    "title": {
                        "type": "string",
                    },
                    "account_id": {
                        "type": "number"
                    }
                },
                "required": ["@controls", "title", "account_id"]
            },
            "name": {
                "type": "string"
            },
            "card_sha": {
                "type": "string"
            }
        },
        "required": ["@controls", "name", "card_sha", "account"]
    }

    validate(json_object, card_mason)


def validate_transaction_mason(json_object):
    transaction_mason = {
        "type": "object",
        "properties": {
            "@controls": {
                "type": "object",
                "properties": {
                    "cr:create-transaction": {
                        "type": "object",
                        "properties": {
                            "encoding": {
                                "type": "string"
                            },
                            "href": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string"
                            },
                            "schema_url": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["encoding", "href", "method", "schema_url", "title"]
                    },
                    "self": {
                        "type": "object",
                        "properties": {
                            "href": {
                                "type": "string"
                            }
                        },
                        "required": ["href"]
                    }
                },
                "required": ["cr:create-transaction", "self"]
            },
            "card": {
                 "type": "object",
                 "properties": {
                     "@controls": {
                         "type": "object",
                         "self": {
                             "type": "object",
                             "properties": {
                                 "href": {
                                     "type": "string"
                                 }
                             },
                             "required": ["href"]
                         }
                     },
                     "card_sha": {
                         "type": "string",
                     },
                     "title": {
                         "type": "string"
                     }
                 },
                 "required": ["@controls", "card_sha", "title"]
            },
            "register": {
                 "type": "object",
                 "properties": {
                     "@controls": {
                         "type": "object",
                         "self": {
                             "type": "object",
                             "properties": {
                                 "href": {
                                     "type": "string"
                                 }
                             },
                             "required": ["href"]
                         }
                     },
                     "register_sha": {
                         "type": "string",
                     },
                     "title": {
                         "type": "string"
                     }

                 },
                 "required": ["@controls", "register_sha", "title"]
            },
            "timestamp": {
                "type": "string"
            },
            "transaction_id": {
                "type": "number"
            }
        },
        "required": ["@controls", "card", "register", "timestamp", "transaction_id"]
    }

    validate(json_object, transaction_mason)



# Testing registers

# GET requests

# Test getting all registers
def test_registers_getall():
    result = testclient.get('registers')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    kahvihuone = jsondata[0]
    assert kahvihuone['name'] == "Kahvihuone"


# Test getting single register
def test_registers_get():
    result = testclient.get('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    reg = jsondata

    assert reg['name'] == "Kahvihuone"
    assert reg['register_sha'] == "acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88"
    assert reg['type'] == 0

    validate_register_mason(reg)


# Test getting register that does not exist
def test_registers_get_nonexistent():
    result = testclient.get('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e86')

    assert result.status_code == 404


# POST testing

# Test successfull post
def test_registers_post():

    newregister = {
      "name": "Topcoolnewregister",
      "register_sha": "acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337",
      "type": 0
    }

    result = testclient.post('registers', data=json.dumps(newregister), content_type='application/json')

    assert result.status_code == 201

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    reg = jsondata

    assert reg['name'] == newregister['name']
    assert reg['register_sha'] == newregister['register_sha']
    assert reg['type'] == newregister['type']

    validate_register_mason(reg)


# Test sending broken jsons to post
def test_registers_post_broken_post_data():
    #Broken json 1
    newregisterbrokendata = {
      "nabrokenme": "Topcoolnewregisterssd",
      "register_sha": "acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51331",
      "type": 0
    }

    result = testclient.post('registers', data=json.dumps(newregisterbrokendata), content_type='application/json')
    assert result.status_code == 400

    # Broken json 2
    newregisterbrokendata = {
      "nabrokenme": "Topcoolnewregisterssd",
      "type": 0
    }

    result = testclient.post('registers', data=json.dumps(newregisterbrokendata), content_type='application/json')
    assert result.status_code == 400

    # Broken json 3
    newregisterbrokendata = {
      "nabrokenme": "Topcoolnewregisterssd",
      "register_sha": "acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51331",
      "tydpe": 0
    }

    result = testclient.post('registers', data=json.dumps(newregisterbrokendata), content_type='application/json')
    assert result.status_code == 400


# Test creating register with already existing sha hash key
def test_registers_post_duplicate_sha():
    newregister = {
      "name": "Newuniquename",
      "register_sha": "acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88",
      "type": 0
    }

    result = testclient.post('registers', data=json.dumps(newregister), content_type='application/json')
    assert result.status_code == 409


# Test creating register with invalid types (0 and 1 allowed)
def test_registers_post_invalid_type():
    newregister = {
      "name": "Newuniquename",
      "register_sha": "acdf285126053bcbe7182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88",
      "type": 2
    }

    result = testclient.post('registers', data=json.dumps(newregister), content_type='application/json')
    assert result.status_code == 400

    newregister['type'] = -6
    result = testclient.post('registers', data=json.dumps(newregister), content_type='application/json')
    assert result.status_code == 400

    newregister['type'] = 102843857646728482874728846626754883754673858673664
    result = testclient.post('registers', data=json.dumps(newregister), content_type='application/json')
    assert result.status_code == 400


# Test creating register with too short, empty and too long sha hash key
def test_registers_post_invalid_sha():
    newregister = {
      "name": "Newuniquename",
      "register_sha": "acdf285926053bcbe",
      "type": 0
    }
    result = testclient.post('registers', data=json.dumps(newregister), content_type='application/json')
    assert result.status_code == 400

    newregister['register_sha'] = ""
    result = testclient.post('registers', data=json.dumps(newregister), content_type='application/json')
    assert result.status_code == 400

    newregister['register_sha'] = "acdf285126053bcbe7182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88acdf285126053bcbe7182e18b72062b1fc4d64a3d81e8bff52f399f956a57e884d64a3d81e8bff52f399f956a57e88"
    result = testclient.post('registers', data=json.dumps(newregister), content_type='application/json')
    assert result.status_code == 400


# Test creating register with empty and too long name
def test_registers_post_invalid_name():
    newregister = {
      "name": "",
      "register_sha": "acdf285126053bcbe7182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88",
      "type": 0
    }

    result = testclient.post('registers', data=json.dumps(newregister), content_type='application/json')
    assert result.status_code == 400

    newregister['name'] = "aklsfdjlasdjflkjasdlfkjaslkdfj lksajdflkjsadfjasölkdjf aksljdf lkasjdflk jaskldfj aslkdjflkasj dfkljasflkj "

    result = testclient.post('registers', data=json.dumps(newregister), content_type='application/json')
    assert result.status_code == 400


# Test creating register with already existing name
def test_registers_post_duplicate_name():
    newregister = {
      "name": "Kahvihuone",
      "register_sha": "acdf285126053bcbe7182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88",
      "type": 0
    }

    result = testclient.post('registers', data=json.dumps(newregister), content_type='application/json')
    assert result.status_code == 409


# PATCH requests

# Test successfull patch
def test_registers_patch():
    patchdata = {
      "name": "Newpatchname",
      "type": 1
    }

    result = testclient.patch('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337', data=json.dumps(patchdata), content_type='application/json')
    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    reg = jsondata

    assert reg['name'] == patchdata['name']
    assert reg['type'] == patchdata['type']

    validate_register_mason(reg)


# Test updating register that does not exist
def test_registers_patch_register_not_exist():
    patchdata = {
      "name": "Newpatchname",
      "type": 1
    }

    result = testclient.patch('registers/acab285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 404


# Test updating register with broken json payload
def test_registers_patch_broken_json():
    patchdata = {

    }

    result = testclient.patch('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337', data=json.dumps(patchdata), content_type='application/json')
    assert result.status_code == 400

    patchdata = {
      "nasme": "Newpatchnameddd",
    }

    result = testclient.patch('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337', data=json.dumps(patchdata), content_type='application/json')
    assert result.status_code == 400


# Test updating register with too long and empty name
def test_register_patch_invalid_name():
    patchdata = {
      "name": "Newpatchnamedsklafjkl asjdfl jaslkdöf jlksajdflökjs fljsölkdf jlöksajdf klsa jdflkj skldfjl skdjflksj f"
    }

    result = testclient.patch('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337', data=json.dumps(patchdata), content_type='application/json')
    assert result.status_code == 400

    patchdata = {
      "name": ""
    }

    result = testclient.patch('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337', data=json.dumps(patchdata), content_type='application/json')
    assert result.status_code == 400


# Test updating register to name that already exists
def test_register_patch_duplicate_name():
    patchdata = {
      "name": "Kahvihuone"
    }

    result = testclient.patch('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337', data=json.dumps(patchdata), content_type='application/json')
    assert result.status_code == 409


# Test updating to register to invalid type (only 0 and 1 are allowed)
def test_register_patch_invalid_type():
    patchdata = {
      "type": -6
    }

    result = testclient.patch('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337', data=json.dumps(patchdata), content_type='application/json')
    assert result.status_code == 400

    patchdata = {
      "type": ""
    }

    result = testclient.patch('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337', data=json.dumps(patchdata), content_type='application/json')
    assert result.status_code == 400

    patchdata = {
      "type": 2
    }

    result = testclient.patch('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337', data=json.dumps(patchdata), content_type='application/json')
    assert result.status_code == 400

    patchdata = {
      "type": 87345897348567892349872398479238759823759873298579834598
    }

    result = testclient.patch('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337', data=json.dumps(patchdata), content_type='application/json')
    assert result.status_code == 400


# DELETE reguest testing


# Test successfull delete
def test_registers_delete():
    result = testclient.delete('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337')

    assert result.status_code == 200


# Test deleting register that does not exist
def test_registers_delete_nonexistent():
    result = testclient.delete('registers/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a51337')

    assert result.status_code == 404


# Testing cards


# GET requests


# Test getting all cards
def test_card_get():
    result = testclient.get('cards')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    card = jsondata[0]

    assert card['name'] == "Opiskelijakortti"


# Test getting single card
def test_card_get_by_id():
    result = testclient.get('cards/8a1470b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    card = jsondata

    assert card['name'] == "Opiskelijakortti"

    validate_card_mason(card)


# Test getting card that does not exist
def test_card_get_by_id_not_exist():
    result = testclient.get('cards/8a1470b1f84c72f2a733ba485f67a3ec30bdddf2ddce574493cb0365107fc148')

    assert result.status_code == 404


# Test getting all unassigned cards
def test_card_get_unassigned():
    result = testclient.get('cards/unassigned')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    card = jsondata[0]

    assert card['name'] == "Orpokortti"


# POST requests

# Testing successful post
def test_card_post():
    postdata = {
        "card_sha": "8a1337b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148",
        "name": "Uusivaliditestikortti",
        "account_id": 5
    }

    result = testclient.post('cards', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 201

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    card = jsondata

    validate_card_mason(card)


# Test creating card with empty and too long name
def test_card_post_invalid_name():
    postdata = {
        "card_sha": "8a1337b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb036513371337",
        "name": ""
    }

    result = testclient.post('cards', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400


    postdata = {
        "card_sha": "8a1337b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb036513371337",
        "name": "jaslkfjöl sakjföl asjdföaslk fj lkasdj flkasj fdlkjsa lfj aslkfdjlaksdjfl kasdjfklasjfdlkasjd flökjsadflk jasdlkfj sadlkfj lkasdjföksldfj ölk"
    }

    result = testclient.post('cards', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400


# Test creating new card to account that already has card with same name
def test_card_post_duplicate_card_name_within_account():
    postdata = {
        "card_sha": "133737b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb036513371337",
        "name": "Opiskelijakortti",
        "account_id": 1
    }

    result = testclient.post('cards', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 409


# Test creating card to account that does not exist
def test_card_post_invalid_account():
    postdata = {
        "card_sha": "8a1337b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb036513371337",
        "account_id": 1337
    }

    result = testclient.post('cards', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 412


# Test creating card with too short and too long sha hash key
def test_card_post_invalid_sha():
    postdata = {
        "card_sha": "8a1337b1f84c72f2a7"
    }

    result = testclient.post('cards', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400

    postdata = {
        "card_sha": "8a1337b1f84c72f2a7asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfsadfasdfasdfsadfasdfasdfasdfsafasdfasdfasdfasdfasdfsadf"
    }

    result = testclient.post('cards', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400


# Test creating card with sha hash key that already exists
def test_card_post_duplicate_sha():
    postdata = {
        "card_sha": "8a1337b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148"
    }

    result = testclient.post('cards', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 409


# PATCH requests

# Test successful card patch
def test_card_patch():
    patchdata = {
      "name": "Okortti21"
    }
    result = testclient.patch('cards/8a1470b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 200

    patchdata = {
      "name": "Opiskelijakortti"
    }
    result = testclient.patch('cards/8a1470b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    card = jsondata

    validate_card_mason(card)


# Test updating card that does not exist
def test_card_patch_card_not_exist():
    patchdata = {
      "name": "nimiolemattomallekortille"
    }
    result = testclient.patch('cards/133770b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 404


# Test updating card to be assigned to nonexistent account
def test_card_patch_new_account_not_exist():
    patchdata = {
        "account_id": 1337
    }

    result = testclient.patch('cards/8a1470b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 412


# Test updating card to be assigned to account that already has card with this name
def test_card_patch_new_account_has_duplicate_card_name():
    patchdata = {
      "account_id": 2
    }

    result = testclient.patch('cards/8a1470b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 409


# Test updating card to have duplicate name within account
def test_card_patch_duplicate_name():
    patchdata = {
      "name": "Kännykkä"
    }

    result = testclient.patch('cards/8a1470b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 409


# Test updating card with empty and too long name
def test_card_patch_invalid_name():
    patchdata = {
      "name": ""
    }
    result = testclient.patch('cards/8a1470b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 400

    patchdata = {
      "name": "jaslödfj laskjflkajs flkj aslkfjsalkj flkasjflkjaslkjf laksjflkajsflkjalkfjkalsjflkasj dflkjaskljfklasj flkjsdkfalfdks klsadfjklsdfj"
    }

    result = testclient.patch('cards/8a1470b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 400


# DELETE requests


# Test successful delete
def test_card_delete():
    result = testclient.delete('cards/8a1337b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148')

    assert result.status_code == 200


# Test deleting card that does not exist
def test_card_delete_card_not_exist():
    result = testclient.delete('cards/8b1470b1f84c72f2a777ba485f67a3ec30bfddf2ddce574493cb0365107fc148')

    assert result.status_code == 404


# Accounts testing

# GET requests

# Test getting all accounts and test balance of those accounts
def test_account_get():
    result = testclient.get('accounts')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    account1 = jsondata[0]
    account2 = jsondata[1]
    account3 = jsondata[2]

    assert account1['name'] == "Ruokatili"

    assert account1['balance'] == 0.0
    assert account2['balance'] == 19.5
    assert account3['balance'] == 3.4


# Test getting single account
def test_account_get_by_id():
    result = testclient.get('accounts/1')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    account1 = jsondata
    assert account1['name'] == "Ruokatili"

    validate_account_mason(account1)


# Test getting account that do not exist
def test_account_get_account_not_exist():
    result = testclient.get('accounts/14567')

    assert result.status_code == 404


# POST requests

# Test successful post
def test_account_post():
    postdata = {
        "name": "Veronkiertotili",
        "user_id": 5
    }

    result = testclient.post('accounts', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 201

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    account1 = jsondata

    validate_account_mason(account1)


# Test creating account with nonexistent user
def test_account_post_user_not_exist():
    postdata = {
        "name": "Validaccountname",
        "user_id": 1337
    }
    result = testclient.post('accounts', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 412


# Test creating account with already existing name within user
def test_account_post_duplicate_name_within_user():
    postdata = {
        "name": "Viinatili",
        "user_id": 1
    }
    result = testclient.post('accounts', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 409


# Test creating account with empty or too long name
def test_account_post_invalid_name():
    postdata = {
        "name": "",
        "user_id": 1
    }
    result = testclient.post('accounts', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400

    postdata = {
        "name": "asdfasdfasd asdf asdfasdf asdf asdf asdf asd saddf asfd asdf asdf asdfasdf asd asdfasdfas sadfasfd asdf asdf fsadfsdf asdf",
        "user_id": 1
    }
    result = testclient.post('accounts', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400


# Test using account post with broken (=empty) json
def test_account_post_broken_json():
    postdata = {

    }
    result = testclient.post('accounts', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400


# PATCH requests

# Test successful account patch
def test_account_patch():
    patchdata = {
        "name": "Salainenveronkiertotili"
    }
    result = testclient.patch('accounts/6', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    account1 = jsondata

    validate_account_mason(account1)


# Test updating account that does not exist
def test_account_patch_account_not_exist():
    patchdata = {
        "name": "Nimiolemattomalleaccountille"
    }
    result = testclient.patch('accounts/1337', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 404


# Test updating account to be assigned to user that does not exist
def test_account_patch_user_not_exist():
    patchdata = {
        "user_id": 1337
    }
    result = testclient.patch('accounts/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 412


# Test updating account to have already existing name within user
def test_account_patch_new_duplicate_name():
    patchdata = {
        "name": "Viinatili"
    }
    result = testclient.patch('accounts/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 409


# Test assigning account to user that already has account with this name
def test_account_patch_new_user_has_duplicate_name():
    patchdata = {
        "user_id": 2
    }
    result = testclient.patch('accounts/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 409


# Test updating account with empty and too long name
def test_account_patch_invalid_name():
    patchdata = {
        "name": ""
    }
    result = testclient.patch('accounts/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 400

    patchdata = {
        "name": "fad sadf asdf asd fasdf asdf asdf adsf asdf asdf asdf asdf asdfasdf asdf asdfasfd sadf asf sdfasdf asdf asdfadfa sdfasf d"
    }
    result = testclient.patch('accounts/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 400


# Test updating account with broken(=empty) json payload
def test_account_patch_broken_json():
    patchdata = {

    }
    result = testclient.patch('accounts/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 400


# DELETE requests

# Test successful delete
def test_account_delete():
    result = testclient.delete('accounts/6')

    assert result.status_code == 200


# Test deleting account that does not exist
def test_account_delete_account_not_exist():
    result = testclient.delete('accounts/1337')

    assert result.status_code == 404


# Admins testing

# GET requests

# Test getting all admins
def test_admin_get():
    result = testclient.get('admins')

    assert result.status_code == 200


# Test getting single admin
def test_admin_get_by_id():
    result = testclient.get('admins/1')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    admin1 = jsondata

    validate_admin_mason(admin1)


# Test getting admin that does not exist
def test_admin_get_by_id_admin_not_exist():
    result = testclient.get('admins/1337')

    assert result.status_code == 404


# POST requests

# Test successful post
def test_admin_post():
    postdata = {
        "password": "v3rys3cr3t",
        "user_id": 3
    }

    result = testclient.post('admins', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 201

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    admin1 = jsondata

    validate_admin_mason(admin1)


# Test creating admin with empty, too short and too long password
def test_admin_post_invalid_password():
    postdata = {
        "password": "",
        "user_id": 1
    }

    result = testclient.post('admins', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400

    postdata = {
        "password": "123",
        "user_id": 1
    }

    result = testclient.post('admins', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400

    postdata = {
        "password": "1234j askldfj lökasdjfklasj dflk jaslk dfjlkas jlfkj aslkjdf lkasjf dkljsdfklj aslkfdj klsajf kasjfdlksajkfljaskdlfjlkjsf",
        "user_id": 1
    }

    result = testclient.post('admins', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400


# Test creating admin from user that does not exist
def test_admin_post_user_not_exist():
    postdata = {
        "password": "v3rys3cr3t",
        "user_id": 1337
    }

    result = testclient.post('admins', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 412


# Test creating admin from user that is already admin
def test_admin_post_user_is_already_admin():
    postdata = {
        "password": "v3rys3cr3t",
        "user_id": 6
    }

    result = testclient.post('admins', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 409


# PATCH requests

# Test successful patch
def test_admin_patch():
    patchdata = {
        "password": "newvalidpassword11111"
    }

    result = testclient.patch('admins/2', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    admin1 = jsondata

    validate_admin_mason(admin1)


# Test updating admin that does not exist
def test_admin_patch_admin_not_exist():
    patchdata = {
        "password": "newvalidpassword11111"
    }

    result = testclient.patch('admins/1337', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 404


# Test updating admin with empty, too short and too long password
def test_admin_patch_invalid_password():
    patchdata = {
        "password": "",
    }

    result = testclient.patch('admins/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 400

    patchdata = {
        "password": "123",
    }

    result = testclient.patch('admins/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 400

    patchdata = {
        "password": "1234j askldfj lökasdjfklasj dflk jaslk dfjlkas jlfkj aslkjdf lkasjf dkljsdfklj aslkfdj klsajf kasjfdlksajkfljaskdlfjlkjsf",
    }

    result = testclient.patch('admins/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 400


# DELETE requests

# Test successfull admin delete
def test_admin_delete():
    result = testclient.delete('admins/2')

    assert result.status_code == 200

    result = testclient.get('admins/2')

    assert result.status_code == 404


# Test deleting admin that does not exist
def test_admin_delete_admin_not_exist():
    result = testclient.delete('admins/1337')

    assert result.status_code == 404


# Transactions testing

# GET requests

# Test getting all transactions
def test_transactions_get():
    result = testclient.get('transactions')

    assert result.status_code == 200


# Test getting single transaction
def test_transactions_get_by_id():
    result = testclient.get('transactions/1')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    t1 = jsondata

    validate_transaction_mason(t1)


# Test getting nonexistent transaction
def test_transactions_get_transaction_not_exist():
    result = testclient.get('transactions/1337')

    assert result.status_code == 404


# Test getting transactions by card
def test_transactions_get_by_card():
    result = testclient.get('transactions/card/8a1470b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148')

    assert result.status_code == 200


# Test getting transactions of nonexistent card
def test_transactions_get_by_card_not_exist():
    result = testclient.get('transactions/card/8a1470b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc000')

    assert result.status_code == 404


# Test getting transactions by account
def test_transactions_get_by_account():
    result = testclient.get('transactions/account/1')

    assert result.status_code == 200


# Test getting transactions of nonexistent account
def test_transactions_get_by_account_not_exist():
    result = testclient.get('transactions/account/1337')

    assert result.status_code == 404


# Test getting transactions by user
def test_transactions_get_by_user():
    result = testclient.get('transactions/user/1')

    assert result.status_code == 200


# Test getting transactions of nonexistent user
def test_transactions_get_by_user_not_exist():
    result = testclient.get('transactions/user/1337')

    assert result.status_code == 404


# Test getting transactions by register
def test_transactions_get_by_register():
    result = testclient.get('transactions/register/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88')

    assert result.status_code == 200


# Test getting transactions of nonexistent register
def test_transactions_get_by_register_not_exist():
    result = testclient.get('transactions/register/acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e00')

    assert result.status_code == 404


# POST requests

# Test successfull positive and negative transaction creation
def test_transactions_post():

    # Negative balance change, value on card required
    postdata = {
        "balance_change": -1.5,
        "card_sha": "034f5e8d6d75496524c5947923874ed55715989cf4c36b539622085049500336",
        "register_sha": "acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88"
    }

    result = testclient.post('transactions', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 201

    # Positive balance change, admin user required
    postdata = {
        "balance_change": 1.5,
        "card_sha": "034f5e8d6d75496524c5947923874ed55715989cf4c36b539622085049500336",
        "register_sha": "0afb00138d8e73348ec1fe41fd3d3a8fcbd90156b263bfa5791ba0e095f42cfc"
    }

    result = testclient.post('transactions', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 201


# Test getting more money from card that is does have
def test_transactions_invalid_balance():
    postdata = {
        "balance_change": -1000,
        "card_sha": "034f5e8d6d75496524c5947923874ed55715989cf4c36b539622085049500336",
        "register_sha": "acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88"
    }

    result = testclient.post('transactions', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 412


# Test creating transaction for card that does not exist
def test_transactions_card_not_exist():
    postdata = {
        "balance_change": -1.5,
        "card_sha": "888f5e8d6d75496524c5947923874ed55715989cf4c36b539622085049500336",
        "register_sha": "acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88"
    }

    result = testclient.post('transactions', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 412


# Test creating transaction for register that does not exist
def test_transactions_register_not_exist():
    postdata = {
        "balance_change": -1.5,
        "card_sha": "034f5e8d6d75496524c5947923874ed55715989cf4c36b539622085049500336",
        "register_sha": "yyyy285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88"
    }

    result = testclient.post('transactions', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 412


# Test creating transaction for card that is not assigned to account
def test_transactions_card_not_assigned():
    postdata = {
        "balance_change": -1.5,
        "card_sha": "c9c00df9280750d4b207d4739b604aa72c4d040badea5fa5a76779851d13d264",
        "register_sha": "acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88"
    }

    result = testclient.post('transactions', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 412


# Test creating positive transaction from register that is not admin
def test_transactions_register_is_not_admin():
    postdata = {
        "balance_change": 1.5,
        "card_sha": "034f5e8d6d75496524c5947923874ed55715989cf4c36b539622085049500336",
        "register_sha": "acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88"
    }

    result = testclient.post('transactions', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 412


# Users testing


# GET requests

# Test get all users
def test_users_get():
    result = testclient.get('users')

    assert result.status_code == 200


# Test getting single user
def test_users_get_by_id():
    result = testclient.get('users/1')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    user1 = jsondata

    validate_user_mason(user1)


# Test getting nonexistent user
def test_user_get_user_not_exist():
    result = testclient.get('users/1337')

    assert result.status_code == 404


# POST requests

# Test successful post
def test_user_post():
    postdata = {
        "email": "john.doe@example.com",
        "name": "John Doe",
        "phone": "+358400123123"
    }

    result = testclient.post('users', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 201

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    user1 = jsondata

    validate_user_mason(user1)


# Test creating user that has already existing email
def test_user_post_duplicate_email():
    postdata = {
        "email": "matti@matikainen.fi",
        "name": "Duplicateemailuser",
        "phone": "+358400129999"
    }

    result = testclient.post('users', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 409


# Test creating user with empty, invalid or too long email
def test_user_post_invalid_email():
    postdata = {
        "email": "",
        "name": "Invaliduser",
        "phone": "+358400129999"
    }

    result = testclient.post('users', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400

    postdata = {
        "email": "    ",
        "name": "Invaliduser",
        "phone": "+358400129999"
    }

    result = testclient.post('users', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400

    postdata = {
        "email": "kjaksdfjlkasjdflkjaslkfdjalksjfdklajsklfjlksdjkl@asdfkljaslkjflkasjdflkjaslkdfjlkasjdflkjsadlkfjlaksjdflkaskkasjdflkjsalkfj.com",
        "name": "Invaliduser",
        "phone": "+358400129999"
    }

    result = testclient.post('users', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400


# Test creating user with empty or too long name
def test_user_post_invalid_name():
    postdata = {
        "email": "invalid.name@example.com",
        "name": "",
        "phone": "+358400987654"
    }

    result = testclient.post('users', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400

    postdata = {
        "email": "invalid.name@example.com",
        "name": "asdkjflökasdjflkasjdf kasjdkf askdfjlkasdjf laskdjflksjflksjfdlkasjdflkasjdfklasjflk sjdflkjsdflkjsdflkj sdfkjsdklajkl",
        "phone": "+358400987654"
    }

    result = testclient.post('users', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400


# Test creating user with too long phone number
def test_user_post_invalid_phone():
    postdata = {
        "email": "invalid.phone@example.com",
        "name": "John DoeDoeJohn",
        "phone": "+3584001231234567456746745674567465745674567456746746574567456745674567456754675467467"
    }

    result = testclient.post('users', data=json.dumps(postdata), content_type='application/json')

    assert result.status_code == 400


# PATCH requests

# Test successful user patch
def test_user_patch():
    patchdata = {
        "email": "johndoetokatili@example.fi",
        "name": "John Doe2",
        "phone": "+3584001231231"
    }

    result = testclient.patch('users/7', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 200

    json_byte_string = result.data
    json_string = str(json_byte_string, 'utf8')
    jsondata = json.loads(json_string)

    user1 = jsondata

    validate_user_mason(user1)


# Test updating user that does not exist
def test_user_patch_user_not_exist():
    patchdata = {
        "email": "johndoetokatili@example.fi",
        "name": "John Doe2",
        "phone": "+3584001231231"
    }

    result = testclient.patch('users/1337', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 404


# Test updating user to have already existing email
def test_user_patch_duplicate_email():
    patchdata = {
        "email": "mervi@matikainen.fi"
    }

    result = testclient.patch('users/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 409


# Test updating user to have too short or too long email
def test_user_patch_invalid_email():
    patchdata = {
        "email": ""
    }

    result = testclient.patch('users/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 400

    patchdata = {
        "email": "kjaksdfjlkasjdflkjaslkfdjalksjfdklajsklfjlksdjkl@asdfkljaslkjflkasjdflkjaslkdfjlkasjdflkjsadlkfjlaksjdflkaskkasjdflkjsalkfj.com"
    }

    result = testclient.patch('users/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 400


# Test updating user to have empty or too long name
def test_user_patch_invalid_name():
    patchdata = {
        "name": ""
    }

    result = testclient.patch('users/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 400

    patchdata = {
        "name": "asdkjflökasdjflkasjdf kasjdkf askdfjlkasdjf laskdjflksjflksjfdlkasjdflkasjdfklasjflk sjdflkjsdflkjsdflkj sdfkjsdklajkl"
    }

    result = testclient.patch('users/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 400


# Test updating user to have too long phone number
def test_user_patch_invalid_phone():
    patchdata = {
        "phone": "+3584001231234567456746745674567465745674567456746746574567456745674567456754675467467"
    }

    result = testclient.patch('users/1', data=json.dumps(patchdata), content_type='application/json')

    assert result.status_code == 400


# DELETE

# Test successful user deletion
def test_user_delete():
    result = testclient.delete('users/7')

    assert result.status_code == 200


# Test deleting user that does not exist
def test_user_delete_user_not_exist():
    result = testclient.delete('users/1337')

    assert result.status_code == 404

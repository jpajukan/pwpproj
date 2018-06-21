# Cash register system

## Dependencies:
### Virtual machine
* Vagrant 1.8 or newer
* Vagrant-vbguest plugin 0.13.0 or newer
* Virtualbox 5.0 or newer

### OS (for the guest system running on virtual machine)
* Debian 8 Jessie or newer (might work on older versions and other
distributions, but it's not tested. Windows is not nor will be supported.)
* PostgreSQL 9.4 or newer
* Python 3

### Python
* connexion
* Flask-SQLAlchemy
* Flask-HTTPAuth
* passlib
* psycopg2
* ipython
* pytest
* pytest-quickcheck

## Installation
Make sure you've installed all the dependecies listed under *Virtual Machine*
section. Navigate to `vagrant` directory under the project root in terminal and
run `vagrant up`. This sets up the virtual machine with all the necessary
dependencies and the test database.

## Running tests
Inside the `vagrant` directory, run `vagrant ssh` in the terminal. This opens
up terminal on the virtual machine. Inside the virtual machine you can simply
navigate to ~/pwp/server/tests and run command `pytest test_db_api.py` to
execute DB API tests or `pytest test_rest_api.py` to execute REST API tests.

## Starting cash-register server
After installation, Inside the `vagrant` directory, run `vagrant ssh` in the
terminal. This opens up terminal on the virtual machine. Navigate to ~/pwp/server
and run command `./launch_server.sh`
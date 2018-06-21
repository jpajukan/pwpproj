#!/usr/bin/env python3

import os
import readline

from pprint import pprint

from server.app import *
from server.db.api import *

init_db(init_app(add_api=False).app)
os.environ['PYTHONINSPECT'] = 'True'

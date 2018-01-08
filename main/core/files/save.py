import os
import time

import json
import jsonpickle
from cryptography.fernet import Fernet

from main.game.contents.items import Container

key = b'9kuDNxazpWoLSeDo9RBbtcCzaYuCzKbgX5m46MY_gqY='
cipher_suite = Fernet(key)


def save_to_file(file_path, game_save):
    """Encrypts and saves to file_path"""

    if os.path.isfile(file_path):
        os.remove(file_path)
    time.sleep(.003)
    output = open(file_path, 'w')
    json.dump(jsonpickle.encode(game_save), output)
    output.close()
    inp = open(file_path, 'r')
    input_str = inp.read()
    inp.close()
    output = open(file_path, 'w')
    output.write(str(cipher_suite.encrypt(bytes(input_str, "UTF-8"))))
    output.close()


def load_from_file(file_path):
    """Loads from file_path, decrypts, and returns as object"""

    inp = open(file_path, 'r')
    input_str = cipher_suite.decrypt(bytes(inp.read()[2:-1], "UTF-8"))
    inp.close()
    game_save = jsonpickle.decode(json.loads(input_str))
    return game_save

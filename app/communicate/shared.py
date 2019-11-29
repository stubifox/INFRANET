# shared.py

from enum import Enum


class Action(Enum):
    LOAD = 1
    INITIAL = 2
    ENTRY = 3
    LOAD_MORE = 4
    ID = 5
    CHECK = 6
    INSERT_UUID = 7
    UPDATE_THEME = 8
    INSERT = 9


class DictIndex(Enum):
    LOAD = 'load'
    MESSAGE = 'message'
    SENDER = 'sender'
    ID = 'id'
    UUID = 'uuid'
    THEME = 'theme'

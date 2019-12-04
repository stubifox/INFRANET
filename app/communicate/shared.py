"""
 * @author Max Stubenbord
 * @email max.stubi@googlemail.com
 * @create date 2019-11-28 22:50:24
 * @modify date 2019-11-28 22:50:24
 * @desc [description]
"""
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
    ERROR = 'error'
    INFO = 'info'

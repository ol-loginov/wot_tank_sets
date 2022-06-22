# coding=utf-8
import collections
import json
import os
from logging import getLogger

from .constants import CONFIGURATION_FOLDER, DEFAULT_TANK_COLLECTIONS_COUNT, DEFAULT_TANK_COLLECTIONS_LIMIT
from .l10n import l10n
from .util import deep_dict_merge

log = getLogger(__name__)

COLLECTION_LIST_FILE = CONFIGURATION_FOLDER + "/collections.json"
_ICON_PATH_PATTERN = '../maps/icons/mod_wot_tank_groups/%s.png'

_COLLECTION_KEY = 'collection_%d'
_current_settings = {}


# noinspection PyClassHasNoInit
class _KEYS:
    LIMIT = 'limit'


def _restore_defaults(s):
    if _KEYS.LIMIT not in s or not isinstance(s[_KEYS.LIMIT], int):
        s[_KEYS.LIMIT] = DEFAULT_TANK_COLLECTIONS_LIMIT

    for n in range(1, s[_KEYS.LIMIT] + 1):
        c_key = _COLLECTION_KEY % n
        if c_key not in s:
            s[c_key] = {}

        c_default = {
            'enabled': n <= DEFAULT_TANK_COLLECTIONS_COUNT,
            'tanks': []
        }
        s[c_key] = deep_dict_merge(c_default, s[c_key])

    return s


class CollectionData:
    def __init__(self, n, data):
        """
        :param dict data:
        """
        data = data if isinstance(data, collections.Mapping) else {}
        self.enabled = data.get('enabled', True)
        self.title = data.get('title', l10n("tc_%d_title" % n, l10n("tc_generic_title") + " " + str(n)))
        self.tooltip = data.get('tooltip', l10n("tc_%d_tooltip" % n, ''))
        self.icon = data.get('icon', _ICON_PATH_PATTERN % str(n))
        self.tanks = data.get('tanks', [])


class Settings:
    def __init__(self):
        pass

    @staticmethod
    def init():
        saved_settings = {}
        if os.path.exists(COLLECTION_LIST_FILE):
            with open(COLLECTION_LIST_FILE, 'rb') as f_in:
                saved_settings = json.load(f_in, encoding='utf-8')

        global _current_settings
        _current_settings = _restore_defaults(saved_settings)
        log.info("current settings: %s" % repr(_current_settings))

    @staticmethod
    def save():
        if not os.path.exists(CONFIGURATION_FOLDER):
            os.makedirs(CONFIGURATION_FOLDER)

        with open(COLLECTION_LIST_FILE, 'wb') as f_out:
            json.dump(_current_settings, f_out, encoding='utf-8', indent=True, sort_keys=True)

    @staticmethod
    def get_tc_numbers_all():
        return list(range(1, _current_settings[_KEYS.LIMIT] + 1))

    @staticmethod
    def get_tc_numbers_enabled():
        out = []
        for n in Settings.get_tc_numbers_all():
            collection_info = Settings.collection(n)
            if collection_info.enabled:
                out.append(n)
        return out

    @staticmethod
    def get_enabled_collections():
        self = Settings

        out = []
        for n in range(1, _current_settings['limit'] + 1):
            collection_info = self.collection(n)
            if collection_info.enabled:
                out.append((n, collection_info))
        return out

    @staticmethod
    def collection(collection_number):
        key = _COLLECTION_KEY % collection_number
        return CollectionData(collection_number, _current_settings[key])

    @staticmethod
    def add_tank_to_collection(collection_number, tank):
        key = _COLLECTION_KEY % collection_number
        tanks = _current_settings[key]['tanks']
        if tank not in tanks:
            tanks.append(tank)
            Settings.save()

    @staticmethod
    def remove_tank_from_collection(collection_number, tank):
        key = _COLLECTION_KEY % collection_number
        tanks = _current_settings[key]['tanks']
        if tank in tanks:
            tanks.remove(tank)
            Settings.save()

    @staticmethod
    def remove_tank_from_all_collections(tank):
        for n in Settings.get_tc_numbers_all():
            Settings.remove_tank_from_collection(n, tank)

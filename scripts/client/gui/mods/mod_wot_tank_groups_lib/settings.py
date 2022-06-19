# coding=utf-8
import collections
import copy
import json
import os
from logging import getLogger

from .constants import MOD_ID, TANK_COLLECTIONS_NUMBERS, TANK_COLLECTIONS_DEFAULT_COUNT

log = getLogger(__name__)

CONFIGURATION_FOLDER = 'mods/config/%s' % MOD_ID
COLLECTION_LIST_FILE = CONFIGURATION_FOLDER + "/collections.json"

_DEFAULT_ICONS = [
    '../maps/icons/library/bonus_x.png',
    '../maps/icons/library/bons_small.png',
    '../maps/icons/library/badges/24x24/badge_11.png',
    '../maps/icons/library/badges/24x24/badge_12.png',
    '../maps/icons/library/badges/24x24/badge_14.png',
    '../maps/icons/library/badges/24x24/badge_22.png',
    '../maps/icons/library/badges/24x24/badge_23.png',
    '../maps/icons/library/badges/24x24/badge_24.png',
    '../maps/icons/library/badges/24x24/badge_25.png',
    '../maps/icons/library/badges/24x24/badge_84.png',
]

_COLLECTION_KEY = 'collection_%d'
_DEFAULT_SETTINGS = {

}


def _init_defaults():
    for n in TANK_COLLECTIONS_NUMBERS:
        _DEFAULT_SETTINGS[_COLLECTION_KEY % n] = {
            'enabled': n <= TANK_COLLECTIONS_DEFAULT_COUNT,
            'tanks': []
        }


_current_settings = {}


def deep_dict_merge(dct1, dct2, override=True):
    """
    :param dct1: First dict to merge
    :param dct2: Second dict to merge
    :param override: if same key exists in both dictionaries, should override? otherwise ignore. (default=True)
    :return: The merge dictionary
    """
    merged = copy.deepcopy(dct1)
    for k, v2 in dct2.items():
        if k in merged:
            v1 = merged[k]
            if isinstance(v1, dict) and isinstance(v2, collections.Mapping):
                merged[k] = deep_dict_merge(v1, v2, override)
            elif isinstance(v1, list) and isinstance(v2, list):
                merged[k] = v1 + v2
            else:
                if override:
                    merged[k] = copy.deepcopy(v2)
        else:
            merged[k] = copy.deepcopy(v2)
    return merged


class CollectionData:
    def __init__(self, n, data):
        """
        :param dict data:
        """
        data = data if isinstance(data, collections.Mapping) else {}
        self.enabled = data.get('enabled', True)
        self.title = data.get('title', "Tank Collection %d" % (n,))
        self.tooltip = data.get('tooltip', "Ready To Run %d" % (n,))
        self.icon = data.get('icon', _DEFAULT_ICONS[(n - 1) % len(_DEFAULT_ICONS)])
        self.tanks = data.get('tanks', [])


class Settings:
    def __init__(self):
        pass

    @staticmethod
    def init():
        _init_defaults()

        settings_saved = {}
        if os.path.exists(COLLECTION_LIST_FILE):
            with open(COLLECTION_LIST_FILE, 'rb') as f_in:
                settings_saved = json.load(f_in, encoding='utf-8')

        global _current_settings
        _current_settings = deep_dict_merge(_DEFAULT_SETTINGS, settings_saved)

        log.info("current settings: %s" % repr(_current_settings))

    @staticmethod
    def save():
        if not os.path.exists(CONFIGURATION_FOLDER):
            os.makedirs(CONFIGURATION_FOLDER)

        with open(COLLECTION_LIST_FILE, 'wb') as f_out:
            json.dump(_current_settings, f_out, encoding='utf-8', indent=True, sort_keys=True)

    @staticmethod
    def collection(collection_number):
        """
        :param collection_number: 1 .. 12
        :rtype: CollectionData
        """
        key = _COLLECTION_KEY % collection_number
        return CollectionData(collection_number, _current_settings[key])

    @staticmethod
    def add_tank_to_collection(collection_number, tank):
        key = _COLLECTION_KEY % collection_number
        _current_settings[key]['tanks'].append(tank)
        Settings.save()

    @staticmethod
    def remove_tank_from_collection(collection_number, tank):
        key = _COLLECTION_KEY % collection_number
        _current_settings[key]['tanks'].remove(tank)
        Settings.save()

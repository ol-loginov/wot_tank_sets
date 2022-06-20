# coding=utf-8
import collections
import copy
import json
import os
from logging import getLogger

from .constants import MOD_ID, TANK_COLLECTIONS_NUMBERS, TANK_COLLECTIONS_DEFAULT_COUNT, \
    TANK_COLLECTIONS_LIMIT

log = getLogger(__name__)

CONFIGURATION_FOLDER = 'mods/config/%s' % MOD_ID
COLLECTION_LIST_FILE = CONFIGURATION_FOLDER + "/collections.json"
_ICON_PATH_PATTERN = '../maps/icons/mod_wot_tank_groups/%s.png'

_COLLECTION_KEY = 'collection_%d'
_default_settings = {}
_current_settings = {}


def _generate_defaults():
    for n in TANK_COLLECTIONS_NUMBERS:
        _default_settings[_COLLECTION_KEY % n] = {
            'enabled': n <= TANK_COLLECTIONS_DEFAULT_COUNT,
            'tanks': []
        }


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
        self.icon = data.get('icon', _ICON_PATH_PATTERN % str(n))
        self.tanks = data.get('tanks', [])


class Settings:
    def __init__(self):
        pass

    @staticmethod
    def init():
        _generate_defaults()

        saved_settings = {}
        if os.path.exists(COLLECTION_LIST_FILE):
            with open(COLLECTION_LIST_FILE, 'rb') as f_in:
                saved_settings = json.load(f_in, encoding='utf-8')

        global _current_settings
        _current_settings = deep_dict_merge(_default_settings, saved_settings)
        log.info("current settings: %s" % repr(_current_settings))

    @staticmethod
    def save():
        if not os.path.exists(CONFIGURATION_FOLDER):
            os.makedirs(CONFIGURATION_FOLDER)

        with open(COLLECTION_LIST_FILE, 'wb') as f_out:
            json.dump(_current_settings, f_out, encoding='utf-8', indent=True, sort_keys=True)

    @staticmethod
    def get_filter_mappings_all():
        return list(range(1, TANK_COLLECTIONS_LIMIT + 1))

    @staticmethod
    def get_filter_mappings_enabled():
        out = []
        for n in Settings.get_filter_mappings_all():
            collection_info = Settings.collection(n)
            if collection_info.enabled:
                out.append(n)
        return out

    @staticmethod
    def get_enabled_collections():
        self = Settings

        out = []
        for n in range(1, TANK_COLLECTIONS_LIMIT + 1):
            collection_info = self.collection(n)
            if collection_info.enabled:
                out.append((n, collection_info))
        return out

    @staticmethod
    def collection(collection_number):
        """
        :param int collection_number: 1 .. 10
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

# coding=utf-8
import collections
import json
import os
from logging import getLogger

from .constants import CONFIGURATION_FOLDER, DEFAULT_TANK_COLLECTIONS_COUNT, DEFAULT_TANK_COLLECTIONS_LIMIT
from .l10n import l10n, l10n_set_language
from .util import deep_dict_merge, load_json_file, del_key

log = getLogger(__name__)

COLLECTION_LIST_FILE = CONFIGURATION_FOLDER + "/collections.json"
_ICON_PATH_PATTERN = '../maps/icons/mod_editable_tank_sets/%s.png'

_COLLECTION_KEY = 'collection_%d'
_current_settings = {}


# noinspection PyClassHasNoInit
class _KEYS:
    LANG = 'lang'
    LIMIT = 'limit'
    MOD_ENABLED = 'mod_enabled'


def _restore_defaults(s):
    if _KEYS.LIMIT not in s or not isinstance(s[_KEYS.LIMIT], int):
        s[_KEYS.LIMIT] = DEFAULT_TANK_COLLECTIONS_LIMIT
    if _KEYS.MOD_ENABLED not in s or not isinstance(s[_KEYS.MOD_ENABLED], bool):
        s[_KEYS.MOD_ENABLED] = True

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


def _get_file_or_resource(file, resource):
    if os.path.exists(file):
        return '../../../' + file
    return resource


class CollectionData:
    def __init__(self, n, data):
        """
        :param dict data:
        """
        data = data if isinstance(data, collections.Mapping) else {}
        self.enabled = data.get('enabled', True)
        self.title = data.get('title', l10n("tc_generic_title") % n)
        self.tooltip = data.get('tooltip', '')
        self.icon = _get_file_or_resource(CONFIGURATION_FOLDER + "/%d.png" % n, _ICON_PATH_PATTERN % str(n))
        self.tanks = data.get('tanks', [])


class Settings:
    def __init__(self):
        pass

    @staticmethod
    def is_mod_enabled():
        return _current_settings[_KEYS.MOD_ENABLED]

    @staticmethod
    def set_mod_enabled(v):
        _current_settings[_KEYS.MOD_ENABLED] = bool(v)

    @staticmethod
    def set_collection_attributes(n, enabled, title):
        key = _COLLECTION_KEY % n
        if key not in _current_settings:
            _current_settings[key] = dict()

        collection = _current_settings[key]
        if enabled is not None: collection['enabled'] = bool(enabled)
        if title is not None: collection['title'] = str(title)

    @staticmethod
    def init():
        saved_settings = {}
        if os.path.exists(COLLECTION_LIST_FILE):
            saved_settings = load_json_file(COLLECTION_LIST_FILE)

        global _current_settings
        _current_settings = _restore_defaults(saved_settings)
        log.info("current settings: %s" % repr(_current_settings))

        if _KEYS.LANG in _current_settings:
            l10n_set_language(_current_settings[_KEYS.LANG])

        S.reset_ui()

    @staticmethod
    def reset_ui():
        try:
            from .settings_view import reset_ui
            reset_ui()
        except:
            log.exception("cannot connect to settings UI")

    @staticmethod
    def save():
        if not os.path.exists(CONFIGURATION_FOLDER):
            os.makedirs(CONFIGURATION_FOLDER)

        # убираем лишние данные
        for_save = deep_dict_merge({}, _current_settings)
        if _KEYS.MOD_ENABLED in for_save and for_save[_KEYS.MOD_ENABLED]:
            del for_save[_KEYS.MOD_ENABLED]

        for n in S.get_tc_numbers_all():
            save = for_save[_COLLECTION_KEY % n]
            data_save = CollectionData(n, save)
            data_empty = CollectionData(n, {})
            if data_save.title == data_empty.title: del_key(save, 'title')
            if data_save.tooltip == data_empty.tooltip: del_key(save, 'tooltip')

        with open(COLLECTION_LIST_FILE, 'wb') as f_out:
            json.dump(for_save, f_out, encoding='utf-8', indent=True, sort_keys=True)

        S.reset_ui()

    @staticmethod
    def get_collection_limit():
        return _current_settings[_KEYS.LIMIT] if _KEYS.LIMIT in _current_settings else DEFAULT_TANK_COLLECTIONS_LIMIT

    @staticmethod
    def set_collection_limit(n):
        if isinstance(n, int) and n <= 100:
            _current_settings[_KEYS.LIMIT] = n

    @staticmethod
    def get_tc_numbers_all():
        return list(range(1, _current_settings[_KEYS.LIMIT] + 1))

    @staticmethod
    def get_tc_numbers_enabled():
        out = []
        for n in S.get_tc_numbers_all():
            collection_info = S.collection(n)
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
        if tank not in tanks and tank > 0:
            tanks.append(tank)
            S.save()

    @staticmethod
    def remove_tank_from_collection(collection_number, tank):
        key = _COLLECTION_KEY % collection_number
        tanks = _current_settings[key]['tanks']
        if tank in tanks:
            tanks.remove(tank)
            S.save()

    @staticmethod
    def remove_tank_from_all_collections(tank):
        for n in S.get_tc_numbers_all():
            S.remove_tank_from_collection(n, tank)


S = Settings

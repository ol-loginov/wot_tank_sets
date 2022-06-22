import json
import re

from helpers import getClientLanguage
from .constants import MOD_LANGUAGE
from .util import vfs_directory_list, vfs_file_read

_LANGUAGES = {}
_L10N_FOLDER = "gui/mods/mod_wot_tank_sets_lib"

l10_file_pattern = re.compile("^(\w+).json$")
for f in vfs_directory_list(_L10N_FOLDER):
    m = l10_file_pattern.match(f)
    if m is not None:
        _LANGUAGES[m.group(1)] = json.loads(vfs_file_read(_L10N_FOLDER + "/" + f, as_binary=True), encoding='utf-8')

_CLIENT_LANGUAGE = getClientLanguage()
if _CLIENT_LANGUAGE in _LANGUAGES.keys():
    _LANGUAGE = _LANGUAGES[_CLIENT_LANGUAGE]
elif MOD_LANGUAGE in _LANGUAGES.keys():
    _LANGUAGE = _LANGUAGES[MOD_LANGUAGE]
else:
    _LANGUAGE = None


def l10n(key, default=None):
    if default is None: default = key
    if _LANGUAGE is None: return default

    result = default
    if key in _LANGUAGE:
        result = _LANGUAGE[key]
    elif MOD_LANGUAGE in _LANGUAGES and key in _LANGUAGES[MOD_LANGUAGE]:
        result = _LANGUAGES[MOD_LANGUAGE][key]
    return result

import json
import re
from logging import getLogger

from helpers import getClientLanguage
from .constants import MOD_LANGUAGE
from .util import vfs_directory_list, vfs_file_read

log = getLogger(__name__)

_LANGUAGES = {}
_L10N_FOLDER = "gui/mods/mod_editable_tank_sets_lib"

l10_file_pattern = re.compile("^(\w+).json$")
for f in vfs_directory_list(_L10N_FOLDER):
    m = l10_file_pattern.match(f)
    if m is not None:
        _LANGUAGES[m.group(1)] = json.loads(vfs_file_read(_L10N_FOLDER + "/" + f, as_binary=True), encoding='utf-8')

_LANGUAGE = None


def l10n_set_language(lang):
    global _LANGUAGE
    if lang in _LANGUAGES.keys():
        log.info("use language=" + lang)
        _LANGUAGE = _LANGUAGES[lang]
    elif MOD_LANGUAGE in _LANGUAGES.keys():
        log.info("use language=" + MOD_LANGUAGE)
        _LANGUAGE = _LANGUAGES[MOD_LANGUAGE]
    else:
        log.info("use without language")
        _LANGUAGE = None


l10n_set_language(getClientLanguage())


def l10n(key, default=None):
    if default is None: default = key
    if _LANGUAGE is None: return default

    result = default
    if key in _LANGUAGE:
        result = _LANGUAGE[key]
    elif MOD_LANGUAGE in _LANGUAGES and key in _LANGUAGES[MOD_LANGUAGE]:
        result = _LANGUAGES[MOD_LANGUAGE][key]
    return result

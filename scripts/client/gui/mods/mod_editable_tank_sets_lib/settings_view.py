# coding=utf-8
import logging

from .constants import MOD_ID
from .l10n import l10n

log = logging.getLogger(__name__)

_respond_to_save = False
_settings_version = 0


def _on_settings_changed(linkage, new_values):
    global _respond_to_save
    global _settings_version

    from .settings import Settings

    if not _respond_to_save or linkage != MOD_ID:
        return

    def get_key_or_default(ob, key, default):
        return ob[key] if key in ob else default

    def maybe_number(ob):
        try:
            return int(ob) if ob is not None else None
        except TypeError:
            return None

    Settings.set_mod_enabled(new_values['enabled'])
    Settings.set_collection_limit(maybe_number(get_key_or_default(new_values, 'set_limit', None)))
    for n in Settings.get_tc_numbers_all():
        enabled = get_key_or_default(new_values, 'set_%d_enable' % n, None)
        title = get_key_or_default(new_values, 'set_%d_title' % n, None)
        Settings.set_collection_attributes(n, enabled, title)

    log.info("changed in mod settings")
    Settings.save()


def reset_ui():
    global _respond_to_save
    global _settings_version

    from .settings import Settings
    # noinspection PyUnresolvedReferences
    from gui.modsSettingsApi import g_modsSettingsApi
    log.info('mod settings %s: %s' % (type(g_modsSettingsApi), dir(g_modsSettingsApi)))

    mod_settings = {
        'enabled': Settings.is_mod_enabled(),
        'set_limit': Settings.get_collection_limit()
    }
    mod_template = {
        'modDisplayName': l10n('setup.title'),
        'enabled': Settings.is_mod_enabled(),
        'column1': [],
        'column2': [],
    }

    mod_template['column1'].extend([
        {
            'type': 'TextInput',
            'text': l10n('setup.set_limit'),
            'value': Settings.get_collection_limit(),
            'varName': 'set_limit'
        }
    ])
    mod_template['column2'].extend([
        {'type': 'Empty',},
        {'type': 'Empty',},
        {'type': 'Empty',},
        {'type': 'Empty',},
        {'type': 'Empty',},
        {'type': 'Empty',},
    ])

    for n in Settings.get_tc_numbers_all():
        collection = Settings.collection(n)

        var_enable = 'set_%d_enable' % n
        var_title = 'set_%d_title' % n

        mod_settings[var_enable] = collection.enabled
        mod_settings[var_title] = collection.title

        column = mod_template['column1'] if n % 2 == 1 else mod_template['column2']
        column.extend([
            {
                'type': 'CheckBox',
                'text': l10n('setup.set_enabled') % n,
                'value': collection.enabled,
                'varName': var_enable
            },
            {
                'type': 'TextInput',
                'text': None,  # l10n('setup.set_title'),
                'value': collection.title,
                'varName': var_title,
                'width': '400'
            },
            {'type': 'Empty'}
        ])

    # избавляемся от stack overflow
    _respond_to_save = False
    g_modsSettingsApi.updateModSettings(MOD_ID, mod_settings)
    _respond_to_save = True

    # если мы не первый раз туда залазим, то неплохо бы сначала снять listener. иначе быстро быстро будут лететь ивенты
    g_modsSettingsApi.onSettingsChanged -= _on_settings_changed
    g_modsSettingsApi.setModTemplate(MOD_ID, mod_template, _on_settings_changed)

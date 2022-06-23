# coding=utf-8
from .constants import MOD_ID
from .l10n import l10n

_respond_to_save = False


def reset_ui():
    global _respond_to_save

    from .settings import Settings as S
    # noinspection PyUnresolvedReferences
    from gui.modsSettingsApi import g_modsSettingsApi

    mod_settings = {
        'enabled': S.is_mod_enabled()
    }
    mod_template = {
        'modDisplayName': l10n('setup.title'),
        'enabled': S.is_mod_enabled(),
        'column1': [],
        'column2': [],
    }

    for n in S.get_tc_numbers_all():
        collection = S.collection(n)

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

    def onModSettingsChanged(linkage, new_values):
        if not _respond_to_save or linkage != MOD_ID:
            return

        def get_key_or_default(ob, key, default):
            return ob[key] if key in ob else default

        S.set_mod_enabled(new_values['enabled'])
        for n in S.get_tc_numbers_all():
            enabled = get_key_or_default(new_values, 'set_%d_enable' % n, None)
            title = get_key_or_default(new_values, 'set_%d_title' % n, None)
            S.set_collection_attributes(n, enabled, title)
        S.save()

    # избавляемся от stack overflow
    _respond_to_save = False
    g_modsSettingsApi.updateModSettings(MOD_ID, mod_settings)
    _respond_to_save = True

    g_modsSettingsApi.setModTemplate(MOD_ID, mod_template, onModSettingsChanged)

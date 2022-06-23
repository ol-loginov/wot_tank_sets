# coding=utf-8
from .constants import MOD_ID
from .l10n import l10n

respond_to_settings_changed = False


def reset_ui():
    global respond_to_settings_changed

    from .settings import Settings as S
    from gui.modsSettingsApi import g_modsSettingsApi

    template = {
        'modDisplayName': l10n('setup.title'),
        'enabled': S.is_mod_enabled(),
        'column1': [],
        'column2': [],
    }

    column1 = template['column1']
    column2 = template['column2']
    for n in S.get_tc_numbers_all():
        collection = S.collection(n)

        column = column1 if n % 2 == 1 else column2
        column.extend([
            {
                'type': 'CheckBox',
                'text': l10n('setup.set_enabled') % n,
                'value': collection.enabled,
                'varName': 'set_%d_enable' % n
            },
            {
                'type': 'TextInput',
                'text': None,  # l10n('setup.set_title'),
                'value': collection.title,
                'varName': 'set_%d_title' % n,
                'width': '400'
            },
            {'type': 'Empty'}
        ])

    # временно выключим отклик на обновление, чтобы не свалится в stack overflow
    respond_to_settings_changed = False

    def onModSettingsChanged(linkage, new_values):
        if not respond_to_settings_changed or linkage != MOD_ID: return

        def get_key_or_default(ob, key, default):
            return ob[key] if key in ob else default

        S.set_mod_enabled(new_values['enabled'])
        for n in S.get_tc_numbers_all():
            enabled = get_key_or_default(new_values, 'set_%d_enable' % n, None)
            title = get_key_or_default(new_values, 'set_%d_title' % n, None)
            S.set_collection_attributes(n, enabled, title)
        S.save()

    g_modsSettingsApi.updateModSettings(MOD_ID, {'enabled': S.is_mod_enabled()})
    g_modsSettingsApi.setModTemplate(MOD_ID, template, onModSettingsChanged)

    respond_to_settings_changed = True

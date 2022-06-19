import logging

from account_helpers.settings_core.ServerSettingsManager import ServerSettingsManager

from .events import overrideMethod

log = logging.getLogger(__name__)


@overrideMethod(ServerSettingsManager, 'getSection')
def _ServerSettingsManager_getSection(base, self, section, *args, **kwargs):
    res = base(section, *args, **kwargs)
    # if is_carousel_filter_client_section(section):
    #     try:
    #         filterData = simplejson.loads(userprefs.get(USERPREFS.CAROUSEL_FILTERS, '{}'))
    #         prefs = filterData.get('prefs', [])
    #     except:
    #         log.exception('cannot load user preferences')
    #         prefs = []
    #     res.update({x: int(x in prefs) for x in PREFS.XVM_KEYS})
    return res


@overrideMethod(ServerSettingsManager, 'setSections')
def _ServerSettingsManager_setSections(base, self, sections, settings):
    # for section in sections:
    #     if section in _SUPPORTED_SECTIONS:
    #         try:
    #             prefs = [key for key, value in settings.iteritems() if key in PREFS.XVM_KEYS and value]
    #             settings = {key: value for key, value in settings.iteritems() if key not in PREFS.XVM_KEYS}
    #             userprefs.set(USERPREFS.CAROUSEL_FILTERS, simplejson.dumps({'prefs': prefs}, separators=(',', ':')))
    #         except Exception as ex:
    #             err(traceback.format_exc())
    return base(self, sections, settings)

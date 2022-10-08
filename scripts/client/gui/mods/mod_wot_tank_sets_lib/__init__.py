import logging

log = logging.getLogger(__name__)


def _move_old_configs():
    from .constants import MOD_ID, CONFIGURATION_FOLDER
    import os

    wrong_configuration_folder = 'mods/config/%s' % MOD_ID
    if os.path.exists(wrong_configuration_folder) and not os.path.exists(CONFIGURATION_FOLDER):
        log.info("rename wrong config folder " + wrong_configuration_folder + ' to ' + CONFIGURATION_FOLDER)
        os.makedirs(os.path.dirname(CONFIGURATION_FOLDER))
        os.rename(wrong_configuration_folder, CONFIGURATION_FOLDER)


def _load_settings():
    log.info('load settings...')
    from .settings import Settings

    Settings.init()
    log.info('settings loaded!')


# noinspection PyUnresolvedReferences
def _advise():
    log.info('override methods...')

    from ._gui__Scaleform__daapi__view__common__filter_popover import LOADED
    from ._gui__Scaleform__daapi__view__common__vehicle_carousel__carousel_filter import LOADED
    from ._account_helpers__accountsettings import LOADED
    from ._gui__Scaleform__daapi__view__lobby__hangar__hangar_cm_handlers import LOADED
    from ._gui__Scaleform__daapi__view__lobby__techtree__research_cm_handlers import LOADED

    log.info('override methods complete')


def init():
    _move_old_configs()
    _load_settings()
    _advise()

import logging

log = logging.getLogger(__name__)


def _move_old_configs():
    from .constants import MOD_ID, CONFIGURATION_FOLDER
    import os

    wrong_configuration_folders = [
        'mods/config/%s' % MOD_ID,
        'mods/configs/%s' % MOD_ID
    ]
    for wrong_configuration_folder in wrong_configuration_folders:
        if os.path.exists(wrong_configuration_folder) and not os.path.exists(CONFIGURATION_FOLDER):
            if not os.path.exists(os.path.dirname(CONFIGURATION_FOLDER)):
                log.info("create folder " + os.path.dirname(CONFIGURATION_FOLDER) + ' (in ' + os.getcwd() + ')')
                os.makedirs(os.path.dirname(CONFIGURATION_FOLDER))
            log.info("move folder " + wrong_configuration_folder + ' to ' + CONFIGURATION_FOLDER + ' (in ' + os.getcwd() + ')')
            os.rename(wrong_configuration_folder, CONFIGURATION_FOLDER)
            if not os.path.exists(CONFIGURATION_FOLDER):
                log.error('correct configuration folder does not exist')


def _load_settings():
    log.info('load settings...')
    from .settings import Settings

    Settings.init()
    log.info('settings loaded!')


# noinspection PyUnresolvedReferences
def _advise():
    log.info('override methods...')

    from ._gui__filters__carousel_filter import LOADED
    from ._account_helpers__accountsettings import LOADED
    from ._gui__Scaleform__daapi__view__lobby__hangar__hangar_cm_handlers import LOADED
    from ._gui__Scaleform__daapi__view__lobby__techtree__research_cm_handlers import LOADED
    from ._gui__shared__tooltips__filter__VehicleFilterTooltip import LOADED
    from ._gui__Scaleform__daapi__view__common__filter_popover import LOADED
    from .EditableTankSetsModel import LOADED

    log.info('override methods complete')


def init():
    _move_old_configs()
    _load_settings()
    _advise()

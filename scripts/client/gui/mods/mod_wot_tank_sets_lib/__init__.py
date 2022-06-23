import logging

log = logging.getLogger(__name__)


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

    log.info('override methods complete')


def init():
    _load_settings()
    _advise()

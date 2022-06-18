import logging

log = logging.getLogger(__name__)


# noinspection PyUnresolvedReferences
def advise():
    log.info('override methods...')

    from ._gui__Scaleform__daapi__view__common__filter_popover import LOADED
    from ._gui__Scaleform__daapi__view__common__vehicle_carousel__carousel_filter import LOADED
    from ._gui__Scaleform__daapi__view__lobby__hangar__carousels__basic__tank_carousel import LOADED
    from ._account_helpers__accountsettings import LOADED

    log.info('override methods complete')

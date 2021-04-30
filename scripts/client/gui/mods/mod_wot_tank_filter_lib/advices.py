import logging

log = logging.getLogger(__name__)


def advise():
    log.info('override methods...')

    # noinspection PyUnresolvedReferences
    from .gui_Scaleform_daapi_view_common_vehicle_carousel_carousel_filter import LOADED
    # noinspection PyUnresolvedReferences
    from .gui_Scaleform_daapi_view_lobby_hangar_carousels_basic_tank_carousel import LOADED
    # noinspection PyUnresolvedReferences
    from .gui_Scaleform_daapi_view_common_filter_popover import LOADED

    log.info('override methods complete')

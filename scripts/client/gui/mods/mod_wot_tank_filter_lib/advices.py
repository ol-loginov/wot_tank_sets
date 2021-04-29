import logging

log = logging.getLogger(__name__)


# noinspection PyUnresolvedReferences
def advise():
    log.info('override methods...')

    from .mod_tank_carousel import TANK_CAROUSEL_MODIFIED
    from .mod_carousel_filter import CAROUSEL_FILTER_MODIFIED

    log.info('override methods complete')

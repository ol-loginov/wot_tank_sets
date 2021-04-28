import logging

log = logging.getLogger(__name__)


def advise():
    log.info('override methods...')

    # noinspection PyUnresolvedReferences
    from .tank_carousel_proxy import TANK_CAROUSEL_PROXY

    log.info('override methods complete')

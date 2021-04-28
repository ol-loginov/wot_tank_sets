import logging

log = logging.getLogger(__name__)


def start_debug():
    try:
        import bwpydevd
        bwpydevd.startDebug()
    except Exception as e:
        log.exception(e)
        log.error('Debug error!', exc_info=e)


def startup():
    log.info('Welcome to WoT Tank Filter!')

    import wot_tank_filter_lib.tank_carousel_proxy as tank_carousel_proxy

    tank_carousel_proxy.advise()
    start_debug()


# startup()

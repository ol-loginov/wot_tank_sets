import logging
import sys

log = logging.getLogger(__name__)


def start_debug():
    import os

    local_folder = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.abspath(os.path.join(local_folder, '../../../../')))

    try:
        import bwpydevd
        bwpydevd.startDebug()
    except Exception as e:
        log.exception(e)
        log.error('Debug error!', exc_info=e)


def startup():
    log.info('Welcome to WoT Tank Filter!')
    start_debug()

    from mod_wot_tank_filter_lib.advices import advise

    advise()


startup()

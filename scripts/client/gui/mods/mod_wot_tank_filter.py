import logging
import sys

log = logging.getLogger(__name__)

DEBUG = True
DEBUG_WOT_DECOMPILED_SOURCE_RES = 'C:/Projects/WorldOfTanks-Decompiled/source/res'
DEBUG_MOD_SOURCE_ROOT = 'C:/Games/World_of_Tanks_RU/res_mods/1.17.0.0'


def start_debug():
    import os

    # add local source folder
    sys.path.append(os.path.abspath(DEBUG_MOD_SOURCE_ROOT))
    # add local source folder
    sys.path.append(os.path.abspath(DEBUG_WOT_DECOMPILED_SOURCE_RES))

    try:
        import bwpydevd
        bwpydevd.startDebug()
        # bwpydevd.startPyDevD('pycharm', suspend=True)
    except Exception as e:
        log.exception(e)
        log.error('Debug error!', exc_info=e)


def startup():
    log.info('Welcome to WoT Tank Filter!')

    if DEBUG:
        start_debug()

    from mod_wot_tank_filter_lib.advices import advise

    advise()


startup()

import logging
import sys

log = logging.getLogger(__name__)

DEBUG = False
DEBUG_WOT_DECOMPILED_SOURCE_RES = 'C:/Projects/WorldOfTanks-Decompiled/source/res'
DEBUG_MOD_SOURCE_ROOT = 'C:/Games/World_of_Tanks_RU/res_mods/1.17.0.1'


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


# noinspection PyBroadException
def startup():
    if DEBUG:
        start_debug()

    log.info('Welcome to WoT Tank Filter!')

    try:
        from mod_wot_tank_sets_lib.settings import Settings
        Settings.init()
    except:
        log.exception("cannot initialize settings")
        return

    try:
        from mod_wot_tank_sets_lib.advices import advise
        advise()
    except:
        log.exception("cannot advise to code")
        return


startup()

import logging
import sys

log = logging.getLogger(__name__)


def start_debug():
    try:
        import os
        import bwpydevd

        from mod_editable_tank_sets_lib.constants import CONFIGURATION_FOLDER
        from mod_editable_tank_sets_lib.util import load_json_file

        if not os.path.exists(CONFIGURATION_FOLDER + "/debug"):
            return

        for path in load_json_file(CONFIGURATION_FOLDER + "/debug"):
            sys.path.append(os.path.abspath(path))

        bwpydevd.startDebug()
        # bwpydevd.startPyDevD('pycharm', suspend=True)
    except Exception as e:
        log.exception(e)
        log.error('Debug error!', exc_info=e)


# noinspection PyBroadException
def startup():
    start_debug()

    log.info('Welcome to WoT Tank Filter!')

    try:
        from mod_editable_tank_sets_lib import init
        init()
    except:
        log.exception("cannot start")
        return


startup()

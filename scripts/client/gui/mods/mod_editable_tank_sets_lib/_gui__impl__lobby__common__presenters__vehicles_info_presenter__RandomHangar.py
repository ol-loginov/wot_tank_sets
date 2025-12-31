import logging
import time

from future.utils import viewkeys
from gui.shared.utils.requesters.ItemsRequester import RequestCriteria, PredicateCondition

from gui.impl.lobby.hangar.random.random_hangar import RandomHangar
from .events import overrideMethod
from .settings import Settings as S

log = logging.getLogger(__name__)


def is_in_active_collection(item):
    if not S.is_mod_enabled():
        return True

    # log.info('test: %s invID: %s' % (item, item.invID))
    # log.info('test %s' % (item.invID,))
    return S.is_in_active_collection(item.invID)


IS_IN_ACTIVE_SET_CONDITION = PredicateCondition(lambda item: is_in_active_collection(item))
IS_IN_ACTIVE_SET = RequestCriteria(IS_IN_ACTIVE_SET_CONDITION)


def replace_condition(criteria, plus):
    conditions = list(criteria.conditions)
    conditions = [c for c in conditions if c is not plus] + [plus]
    return RequestCriteria(*conditions)


@overrideMethod(RandomHangar, '_onLoading')
def RandomHangar__onLoading(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)
    if type(self) is not RandomHangar:
        return ret

    log.info("RandomHangar__onLoading %s" % (args,))
    filter = self._RandomHangar__randomVehicleFilter
    filter._setCriteria(replace_condition(filter.criteria, IS_IN_ACTIVE_SET_CONDITION))
    # for cond in filter.criteria.conditions:
    #     log.info("   loading pred: %s" % (cond,))

    filter = self._RandomHangar__randomInvVehicleFilter
    filter._setCriteria(replace_condition(filter.criteria, IS_IN_ACTIVE_SET_CONDITION))

    return ret


@overrideMethod(RandomHangar, '_subscribe')
def RandomHangar__subscribe(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)
    if type(self) is not RandomHangar:
        return ret

    log.info("RandomHangar__subscribe %s" % (args,))

    def special_callback():
        # ts = time.time()

        invFilter = self._RandomHangar__randomInvVehicleFilter
        # oldVehiclesCDs = set(invFilter._vehicles)
        invFilter._setCriteria(replace_condition(invFilter.criteria, IS_IN_ACTIVE_SET_CONDITION))

        # newVehiclesCDS = viewkeys(invFilter._vehicles)
        # te = time.time()
        # log.info("invFilter criteria changed in %s sec" % (te - ts,))
        # log.info("invFilter vehs old: %s" % (len(oldVehiclesCDs),))
        # log.info("invFilter vehs new: %s" % (len(newVehiclesCDS),))
        # log.info("invFilter vehs diff: %s" % (oldVehiclesCDs ^ newVehiclesCDS,))

    setattr(self, '__EditableTankSets_onSettingsChanged', special_callback)
    S.onChanged += special_callback

    return ret


@overrideMethod(RandomHangar, '_unsubscribe')
def RandomHangar__unsubscribe(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)
    if type(self) is not RandomHangar:
        return ret

    log.info("RandomHangar__subscribe %s" % (args,))

    S.onChanged -= self.__EditableTankSets_onSettingsChanged
    return ret


LOADED = True

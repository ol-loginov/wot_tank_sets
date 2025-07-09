from logging import getLogger

# noinspection PyUnresolvedReferences
from gui.shared.utils.requesters.ItemsRequester import REQ_CRITERIA

from gui.Scaleform.daapi.view.common.vehicle_carousel.carousel_filter import BasicCriteriesGroup
from .constants import tank_collection_mapping
from .events import overrideMethod
from .settings import Settings as S

log = getLogger(__name__)


@overrideMethod(BasicCriteriesGroup, 'update')
def BasicCriteriesGroup__update(base, self, filters, *args, **kwargs):
    ret = base(self, filters, *args, **kwargs)
    # log.info('filters: ' + repr(filters))

    if S.is_mod_enabled():
        tanks = set()
        has_applied_filter = False
        for n in S.get_tc_numbers_enabled():
            if tank_collection_mapping(n) in filters and filters[tank_collection_mapping(n)]:
                tanks |= set(S.collection(n).tanks)
                has_applied_filter = True

        if has_applied_filter:
            self._criteria |= REQ_CRITERIA.CUSTOM(lambda item: _apply_tank_group_filters(item, tanks))
    return ret


def _apply_tank_group_filters(item, selected_tanks):
    # log.info('filter tank: ' + str(item.invID))
    return item.invID in selected_tanks


LOADED = True

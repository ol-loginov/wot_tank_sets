# coding=utf-8
#
#
# Thanks to # https://gitlab.com/xvm/xvm/blob/master/src/xpm/xvm_tankcarousel/filter_popover.py
#

import logging

from gui.Scaleform.daapi.view.common.common_constants import FILTER_POPOVER_SECTION
from gui.Scaleform.daapi.view.common.filter_popover import TankCarouselFilterPopover
from gui.filters.carousel_filter import BasicCriteriesGroup
from gui.shared.utils.requesters import REQ_CRITERIA
from .constants import tank_collection_mapping
from .events import overrideMethod, overrideClassMethod
from .settings import Settings as S

log = logging.getLogger(__name__)

is_comp7_filter_popover = lambda (self): False

try:
    from gui.Scaleform.daapi.view.battle.filter_popover import Comp7TankCarouselFilterPopover

    log.info("disable VehiclesFilterPopover hooks for Comp7TankCarouselFilterPopover")
    is_comp7_filter_popover = lambda (self): isinstance(self, Comp7TankCarouselFilterPopover)
except:
    log.error("cannot find Comp7TankCarouselFilterPopover")


def enabled_for_self(self):
    if is_comp7_filter_popover(self):
        return False
    return True


@overrideMethod(TankCarouselFilterPopover, '__init__')
def TankCarouselFilterPopover___init__(base, self, *args, **kwargs):
    log.info("TankCarouselFilterPopover___init__")
    return base(self, *args, **kwargs)


@overrideClassMethod(TankCarouselFilterPopover, '_generateMapping')
def TankCarouselFilterPopover__generateMapping(base, _, *args, **kwargs):
    log.info("TankCarouselFilterPopover__generateMapping")
    mapping = base(*args, **kwargs)

    if S.is_mod_enabled():
        mapping[FILTER_POPOVER_SECTION.SPECIALS].extend([tank_collection_mapping(n) for n in S.get_tc_numbers_enabled()])

    return mapping


@overrideMethod(TankCarouselFilterPopover, '_getInitialVO')
def TankCarouselFilterPopover_getInitialVO(base, self, *args, **kwargs):
    log.info("TankCarouselFilterPopover_getInitialVO")
    ret = base(self, *args, **kwargs)

    if S.is_mod_enabled() and enabled_for_self(self):
        special_vo = ret['specials']
        special_mapping = self._mapping[FILTER_POPOVER_SECTION.SPECIALS]

        for n, collection in S.get_enabled_collections():
            filter_index = special_mapping.index(tank_collection_mapping(n))
            filter_vo = special_vo[filter_index]

            tooltip = "{HEADER}%s{/HEADER}" % collection.title
            if collection.tooltip is not None and len(collection.tooltip) > 0:
                tooltip += "{BODY}%s{/BODY}" % collection.tooltip

            filter_vo.update({'value': collection.icon, 'tooltip': tooltip})

    return ret


# @overrideMethod(VehiclesFilterPopover, '_getUpdateVO')
# def VehiclesFilterPopover_getUpdateVO(base, self, *args, **kwargs):
#     return base(self, *args, **kwargs)



@overrideMethod(BasicCriteriesGroup, 'update')
def BasicCriteriesGroup__update(base, self, filters, *args, **kwargs):
    log.info('filters: ' + repr(filters))
    ret = base(self, filters, *args, **kwargs)

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

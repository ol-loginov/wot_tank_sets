# coding=utf-8
#
#
# Thanks to # https://gitlab.com/xvm/xvm/blob/master/src/xpm/xvm_tankcarousel/filter_popover.py
#

import logging

from gui.Scaleform.daapi.view.common.filter_popover import VehiclesFilterPopover, FILTER_SECTION
from .constants import tank_collection_mapping
from .events import overrideMethod, overrideClassMethod
from .settings import Settings as S

log = logging.getLogger(__name__)


@overrideClassMethod(VehiclesFilterPopover, '_generateMapping')
def VehiclesFilterPopover__generateMapping(base, _, *args, **kwargs):
    mapping = base(*args, **kwargs)

    if S.is_mod_enabled():
        mapping[FILTER_SECTION.SPECIALS].extend([tank_collection_mapping(n) for n in S.get_tc_numbers_enabled()])

    return mapping


@overrideMethod(VehiclesFilterPopover, '_getInitialVO')
def _VehiclesFilterPopover_getInitialVO(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)

    special_vo = ret['specials']
    special_mapping = self._VehiclesFilterPopover__mapping[FILTER_SECTION.SPECIALS]

    if S.is_mod_enabled():
        for n, collection in S.get_enabled_collections():
            filter_index = special_mapping.index(tank_collection_mapping(n))
            filter_vo = special_vo[filter_index]

            tooltip = "{HEADER}%s{/HEADER}" % collection.title
            if collection.tooltip is not None and len(collection.tooltip) > 0:
                tooltip += "{BODY}%s{/BODY}" % collection.tooltip

            filter_vo.update({'value': collection.icon, 'tooltip': tooltip})

    return ret


@overrideMethod(VehiclesFilterPopover, '_getUpdateVO')
def _VehiclesFilterPopover_getUpdateVO(base, self, *args, **kwargs):
    return base(self, *args, **kwargs)


LOADED = True

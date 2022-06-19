# coding=utf-8
#
#
# Thanks to # https://gitlab.com/xvm/xvm/blob/master/src/xpm/xvm_tankcarousel/filter_popover.py
#

import logging

from gui.Scaleform.daapi.view.common.filter_popover import VehiclesFilterPopover, _SECTION
from .constants import TANK_COLLECTIONS_FILTERS, TANK_COLLECTIONS_NUMBERS, TANK_COLLECTIONS_FILTER_PREFIX
from .events import overrideMethod, overrideClassMethod
from .settings import Settings

log = logging.getLogger(__name__)


@overrideClassMethod(VehiclesFilterPopover, '_generateMapping')
def VehiclesFilterPopover__generateMapping(base, _, *args, **kwargs):
    mapping = base(*args, **kwargs)
    mapping[_SECTION.SPECIALS].extend(TANK_COLLECTIONS_FILTERS)
    return mapping


@overrideMethod(VehiclesFilterPopover, '_getInitialVO')
def _VehiclesFilterPopover_getInitialVO(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)

    special_vo = ret['specials']
    special_mapping = self._VehiclesFilterPopover__mapping[_SECTION.SPECIALS]
    for n in TANK_COLLECTIONS_NUMBERS:
        filter_index = special_mapping.index(TANK_COLLECTIONS_FILTER_PREFIX + str(n))
        filter_vo = special_vo[filter_index]

        collection = Settings.collection(n)
        filter_vo.update({
            'value': collection.icon,
            'tooltip': "{HEADER}%s{/HEADER}{BODY}%s{/BODY}" % (collection.title, collection.tooltip),
            'enabled': collection.enabled
        })

    return ret


@overrideMethod(VehiclesFilterPopover, '_getUpdateVO')
def _VehiclesFilterPopover_getUpdateVO(base, self, *args, **kwargs):
    return base(self, *args, **kwargs)


LOADED = True

# coding=utf-8
#
#
# Thanks to # https://gitlab.com/xvm/xvm/blob/master/src/xpm/xvm_tankcarousel/filter_popover.py
#

import logging

from constants import USER_GROUP_FILTERS
from gui.Scaleform.daapi.view.common.filter_popover import VehiclesFilterPopover, _SECTION
from .events import overrideMethod, overrideClassMethod

log = logging.getLogger(__name__)


@overrideClassMethod(VehiclesFilterPopover, '_generateMapping')
def VehiclesFilterPopover__generateMapping(base, _, *args, **kwargs):
    mapping = base(*args, **kwargs)
    mapping[_SECTION.SPECIALS].extend(USER_GROUP_FILTERS)
    return mapping


@overrideMethod(VehiclesFilterPopover, '_getInitialVO')
def _VehiclesFilterPopover_getInitialVO(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)

    special_vo = ret['specials']
    special_mapping = self._VehiclesFilterPopover__mapping[_SECTION.SPECIALS]
    for f in USER_GROUP_FILTERS:
        filter_index = special_mapping.index(f)
        filter_vo = special_vo[filter_index]
        filter_vo.update({
            'value': '../maps/icons/library/bonus_x.png',
            'tooltip': "{HEADER}AкцXионный опыт{/HEADER}{BODY}FuF-FuF{/BODY}",
            'enabled': True
        })

    return ret


@overrideMethod(VehiclesFilterPopover, '_getUpdateVO')
def _VehiclesFilterPopover_getUpdateVO(base, self, *args, **kwargs):
    filters = args[0]
    ret = base(self, *args, **kwargs)
    return ret


LOADED = True

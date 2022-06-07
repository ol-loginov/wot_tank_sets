# coding=utf-8
#
#
# Thanks to # https://gitlab.com/xvm/xvm/blob/master/src/xpm/xvm_tankcarousel/filter_popover.py
#

import logging

from gui.Scaleform.daapi.view.common.filter_popover import VehiclesFilterPopover, _SECTION
from .events import (overrideMethod, overrideClassMethod)

log = logging.getLogger(__name__)

USER_GROUP_LIMIT = 10
USER_GROUP_MAPPING_PREFIX = 'usergroup_'


@overrideClassMethod(VehiclesFilterPopover, '_generateMapping')
def VehiclesFilterPopover__generateMapping(base, self, *args, **kwargs):
    mapping = base(*args, **kwargs)
    for i in range(1, USER_GROUP_LIMIT + 1):
        mapping[_SECTION.SPECIALS].append(USER_GROUP_MAPPING_PREFIX + str(i))
    return mapping


@overrideMethod(VehiclesFilterPopover, '_getInitialVO')
def _VehiclesFilterPopover_getInitialVO(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)

    special_vo = ret['specials']
    special_mapping = self._VehiclesFilterPopover__mapping[_SECTION.SPECIALS]
    for i in range(1, USER_GROUP_LIMIT + 1):
        filter_key = USER_GROUP_MAPPING_PREFIX + str(i)
        filter_index = special_mapping.index(filter_key)
        filter_vo = special_vo[filter_index]
        filter_vo.update({
            'value': '../maps/icons/library/bonus_x.png',
            'tooltip': "{HEADER}Aкционный опыт{/HEADER}{BODY}FuF-FuF{/BODY}",
            'enabled': True
        })

    return ret


LOADED = True

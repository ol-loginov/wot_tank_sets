# coding=utf-8
import logging

from gui.Scaleform.daapi.view.common.filter_popover import VehiclesFilterPopover
from .events import (overrideMethod, overrideClassMethod)

log = logging.getLogger(__name__)

FILTER_SECTION_KEY = 'usergroups'
FILTER_SECTION_ID = 9


@overrideClassMethod(VehiclesFilterPopover, '_generateMapping')
def VehiclesFilterPopover__generateMapping(base, self, *args, **kwargs):
    mapping = base(*args, **kwargs)

    mapping[FILTER_SECTION_ID] = [
        FILTER_SECTION_KEY + '0'
    ]
    return mapping


@overrideMethod(VehiclesFilterPopover, '_getInitialVO')
def VehiclesFilterPopover__getInitialVO(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)

    ret[FILTER_SECTION_KEY] = [
        {'selected': False,
         'enabled': True,
         "tooltip": "{HEADER}Aкционный опыт{/HEADER}{BODY}FuF-FuF{/BODY}",
         'value': '../maps/icons/library/bonus_x.png'}
    ]
    ret[FILTER_SECTION_KEY + 'Label'] = 'Тестовый замес!'
    ret[FILTER_SECTION_KEY + 'SectionId'] = FILTER_SECTION_ID
    ret[FILTER_SECTION_KEY + 'SectionVisible'] = True
    return ret


LOADED = True
# https://gitlab.com/xvm/xvm/blob/master/src/xpm/xvm_tankcarousel/filter_popover.py

import traceback
import logging
import json

from gui.impl.gen.view_models.views.lobby.hangar.sub_views.vehicle_filter_model import VehicleFilterModel, FilterSection, RoleSection
from gui.shared.tooltips import ToolTipBaseData
from gui.impl.lobby.hangar.presenters.vehicle_filters_presenter import VehicleFiltersDataProvider
from gui.impl.pub.view_component import ViewComponent
from gui.filters.carousel_filter import FILTER_KEYS
from gui.shared.tooltips.filter import VehicleFilterTooltip
from .events import overrideMethod, overrideClassMethod, overrideProperty
from .settings import Settings as S
from .constants import tank_collection_mapping
from gui.shared.tooltips.common import BlocksTooltipData
from gui.filters.carousel_filter import _CarouselFilter

log = logging.getLogger(__name__)


# @overrideMethod(ViewComponent, '__init__')
# def ViewComponent___init__(base, self, *args, **kwargs):
#     log.info('ViewComponent___init__ %s' % (type(self),))
#     ret = base(self, *args, **kwargs)
    # log.info('ViewComponent___init__ dir %s' % (dir(self),))
    # return ret


# @overrideMethod(BlocksTooltipData, 'getDisplayableData')
# def BlocksTooltipData_getDisplayableData(base, self, *args, **kwargs):
#     log.info('BlocksTooltipData_getDisplayableData')
#     ret = base(self, *args, **kwargs)
#     log.info('BlocksTooltipData_getDisplayableData << %s' % (ret,))
#
#     return ret


# @overrideMethod(ToolTipBaseData, 'getDisplayableData')
# def ToolTipBaseData_getDisplayableData(base, self, *args, **kwargs):
#     ret = base(self, *args, **kwargs)
#     log.info('BlocksTooltipData_getDisplayableData << %s' % (ret,))
#
#     return ret


# @overrideMethod(VehicleFiltersDataProvider, '_generateMappings')
# def VehicleFiltersDataProvider__generateMappings(base, self, *args, **kwargs):
#     log.info('VehicleFiltersDataProvider__generateMappings %s' % (self,))
#     base(self, *args, **kwargs)
#
#     if S.is_mod_enabled():
#         mapping = self._VehicleFiltersDataProvider__mapping
#         mapping[FilterSection.SPECIALS.value].extend([tank_collection_mapping(n) for n in S.get_tc_numbers_enabled()])
#         log.info('>>> MAPPINGS:: %s' % (mapping,))


# @overrideMethod(VehicleFiltersDataProvider, '_onLoading')
# def VehicleFiltersDataProvider__onLoading(base, self, *args, **kwargs):
#     log.info('VehicleFiltersDataProvider__onLoading %s' % (self,))
#     base(self, *args, **kwargs)
#
#     log.info('>>> FILTERS:: %s' % (self.viewModel.getFilters(),))


# @overrideMethod(VehicleFiltersDataProvider, '_VehicleFiltersDataProvider__updateModel')
# def VehicleFiltersDataProvider___updateModel(base, self, *args, **kwargs):
#     log.info('VehicleFiltersDataProvider___updateModel %s' % (self,))
#     base(self, *args, **kwargs)
#
#     filters = self._VehicleFiltersDataProvider__filter.getFilters()
#     log.info('>>> _updateModel: %s' % (json.dumps(self._VehicleFiltersDataProvider__convertToModel(filters)),))


# @overrideMethod(TankCarouselFilterPopover, '_getInitialVO')
# def TankCarouselFilterPopover_getInitialVO(base, self, *args, **kwargs):
#     log.info("TankCarouselFilterPopover_getInitialVO")
#     ret = base(self, *args, **kwargs)
#
#     if S.is_mod_enabled() and enabled_for_self(self):
#         special_vo = ret['specials']
#         special_mapping = self._mapping[FILTER_POPOVER_SECTION.SPECIALS]
#
#         for n, collection in S.get_enabled_collections():
#             filter_index = special_mapping.index(tank_collection_mapping(n))
#             filter_vo = special_vo[filter_index]
#
#             tooltip = "{HEADER}%s{/HEADER}" % collection.title
#             if collection.tooltip is not None and len(collection.tooltip) > 0:
#                 tooltip += "{BODY}%s{/BODY}" % collection.tooltip
#
#             filter_vo.update({'value': collection.icon, 'tooltip': tooltip})
#
#     return ret

LOADED = True

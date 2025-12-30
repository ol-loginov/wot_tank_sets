import logging
from gui.impl.lobby.common.presenters.vehicles_info_presenter import VehiclesInfoPresenter
from gui.filters.carousel_filter import SessionCarouselFilter, EventCriteriesGroup, CriteriesGroup
from frameworks.wulf import ViewModel
from gui.impl.lobby.hangar.base.vehicles_filter_component import VehiclesFilterComponent
from gui.Scaleform.daapi.view.common.common_constants import FILTER_POPOVER_SECTION
from gui.Scaleform.daapi.view.common.filter_popover import TankCarouselFilterPopover
from gui.filters.carousel_filter import BasicCriteriesGroup
from gui.impl.lobby.hangar.presenters.vehicle_filters_presenter import VehicleFiltersDataProvider
from gui.shared.utils.requesters import REQ_CRITERIA
from .constants import tank_collection_mapping
from .events import overrideMethod, overrideClassMethod
from .settings import Settings as S
import traceback
from gui.shared.utils.requesters import ItemsRequester

log = logging.getLogger(__name__)


@overrideClassMethod(VehicleFiltersDataProvider, '_getBaseSpecialSection')
def VehicleFiltersDataProvider__getBaseSpecialSection(base, self, *args, **kwargs):
    ret = base(*args, **kwargs)
    return ret + ['editableTankSets']


@overrideMethod(CriteriesGroup, 'apply')
def CriteriesGroup_apply(base, self, *args, **kwargs):
    log.info("CriteriesGroup_apply %s" % (args,))
    ret = base(self, *args, **kwargs)
    return ret


@overrideMethod(BasicCriteriesGroup, 'update')
def BasicCriteriesGroup_update(base, self, *args, **kwargs):
    log.info("BasicCriteriesGroup_update %s" % (args,))
    ret = base(self, *args, **kwargs)
    return ret


# @overrideMethod(ViewModel, '_setString')
def ViewModel__setString(base, self, *args, **kwargs):
    log.info("ViewModel__setString %s" % (args,))
    ret = base(self, *args, **kwargs)
    return ret


# @overrideMethod(ViewModel, '_setViewModel')
def ViewModel__setViewModel(base, self, *args, **kwargs):
    log.info("ViewModel__setViewModel %s" % (args,))
    ret = base(self, *args, **kwargs)
    return ret


# @overrideMethod(ViewModel, '_setArray')
def ViewModel__setArray(base, self, *args, **kwargs):
    log.info("ViewModel__setArray %s" % (args,))
    ret = base(self, *args, **kwargs)
    return ret


# @overrideMethod(ViewModel, '_setMap')
def ViewModel__setMap(base, self, *args, **kwargs):
    log.info("ViewModel__setMap %s" % (args,))
    ret = base(self, *args, **kwargs)
    return ret


@overrideMethod(VehiclesFilterComponent, '_VehiclesFilterComponent__createVehiclesDict')
def VehiclesFilterComponent__createVehiclesDict(base, self, *args, **kwargs):
    log.info("VehiclesFilterComponent__createVehiclesDict %s" % (args,))

    for cond in self.criteria.conditions:
        log.info("   pred: %s" % (cond,))

    # traceback.print_stack()
    ret = base(self, *args, **kwargs)
    return ret


@overrideMethod(VehiclesInfoPresenter, '_toModelItem')
def VehiclesInfoPresenter__toModelItem(base, self, *args, **kwargs):
    log.info("VehiclesInfoPresenter__toModelItem %s" % (args,))
    # traceback.print_stack()
    ret = base(self, *args, **kwargs)

    if S.has_active_collections():
        ret['favourite'] = S.is_in_active_collection(ret['inventoryId'])

    return ret


from gui.impl.lobby.hangar.random.random_hangar import RandomHangar, RANDOM_MODE_CRITERIA
from ._gui__filters__carousel_filter import IS_IN_ACTIVE_SET


# @overrideMethod(RandomHangar, '__init__')
# def RandomHangar___init__(base, self, *args, **kwargs):
#     log.info("RandomHangar___init__ %s" % (args,))
#     ret = base(self, *args, **kwargs)
#
#     filter = self._RandomHangar__randomVehicleFilter
#     for cond in filter.criteria.conditions:
#         log.info("   pred: %s" % (cond,))
#
#     self._RandomHangar__randomVehicleFilter = VehiclesFilterComponent(filter.criteria | IS_IN_ACTIVE_SET)
#     return ret


LOADED = True

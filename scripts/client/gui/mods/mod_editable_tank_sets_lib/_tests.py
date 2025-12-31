import logging

from gui.impl.lobby.common.presenters.vehicles_info_presenter import VehiclesInfoPresenter
from .events import overrideMethod
from .settings import Settings as S

log = logging.getLogger(__name__)


# @overrideMethod(ViewModel, '_setString')
def ViewModel__setString(base, self, *args, **kwargs):
    log.info("ViewModel__setString %s" % (args,))
    ret = base(self, *args, **kwargs)
    return ret


# @overrideMethod(ViewModel, '_setResource')
def ViewModel__setResource(base, self, *args, **kwargs):
    log.info("ViewModel__setResource %s" % (args,))
    ret = base(self, *args, **kwargs)
    return ret


# @overrideMethod(VehiclesFilterComponent, '_VehiclesFilterComponent__createVehiclesDict')
def VehiclesFilterComponent__createVehiclesDict(base, self, *args, **kwargs):
    log.info("VehiclesFilterComponent__createVehiclesDict %s" % (args,))

    for cond in self.criteria.conditions:
        log.info("   pred: %s" % (cond,))

    ret = base(self, *args, **kwargs)
    return ret


# import traceback


# @overrideMethod(VehiclesInfoPresenter, '_toModelItem')
def VehiclesInfoPresenter__toModelItem(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)

    # if S.has_active_collections():
    #     ret['favorite'] = S.is_in_active_collection(ret['inventoryId'])
    # traceback.print_stack()

    log.info("VehiclesInfoPresenter__toModelItem %s" % (ret,))
    return ret


# @overrideMethod(VehiclesInfoPresenter, '_VehiclesInfoPresenter__onUpdateVehicles')
def VehiclesInfoPresenter___onUpdateVehicles(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)

    # if S.has_active_collections():
    #     ret['favorite'] = S.is_in_active_collection(ret['inventoryId'])
    # traceback.print_stack()

    log.info("VehiclesInfoPresenter__onUpdateVehicles %s" % (args,))
    log.info("VehiclesInfoPresenter__onUpdateVehicles >> %s" % (self.viewModel.getVehicles().keys(),))
    return ret


LOADED = True

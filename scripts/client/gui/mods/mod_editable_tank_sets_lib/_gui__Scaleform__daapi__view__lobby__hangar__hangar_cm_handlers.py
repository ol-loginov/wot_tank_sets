from logging import getLogger

from gui.Scaleform.daapi.view.lobby.hangar.carousels.basic.tank_carousel import TankCarousel
from gui.Scaleform.daapi.view.lobby.hangar.hangar_cm_handlers import VehicleContextMenuHandler
from .vehicle_cm_additional import setLastCarousel, define_cm_handler_methods, generate_cm_instance_options
from .events import overrideMethod
from .settings import Settings as S

log = getLogger(__name__)

_CMAdditionalHandlers = {}


@overrideMethod(TankCarousel, '__init__')
def TankCarousel___init__(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)
    setLastCarousel(self)
    return ret


@overrideMethod(VehicleContextMenuHandler, '__init__')
def VehicleContextMenuHandler___init__(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)
    self._AbstractContextMenuHandler__handlers.update(_CMAdditionalHandlers)
    return ret


@overrideMethod(VehicleContextMenuHandler, '_generateOptions')
def VehicleContextMenuHandler__generateOptions(base, self, *args, **kwargs):
    options = base(self, *args, **kwargs)
    generate_cm_instance_options(self, self.getVehInvID(), options)
    return options


define_cm_handler_methods(VehicleContextMenuHandler, _CMAdditionalHandlers)
LOADED = True

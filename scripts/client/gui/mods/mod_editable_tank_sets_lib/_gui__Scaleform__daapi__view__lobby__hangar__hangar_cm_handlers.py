from logging import getLogger

from gui.Scaleform.daapi.view.lobby.hangar.hangar_cm_handlers import VehicleContextMenuHandler
from .context_menus import define_cm_handler_methods, generate_cm_instance_options
from .events import overrideMethod

log = getLogger(__name__)

_CMAdditionalHandlers = {}


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

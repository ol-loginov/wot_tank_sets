from gui.Scaleform.daapi.view.lobby.techtree.research_cm_handlers import ResearchVehicleContextMenuHandler
from .events import overrideMethod
from .vehicle_cm_additional import define_cm_handler_methods, generate_cm_instance_options

_CMAdditionalHandlers = {}


@overrideMethod(ResearchVehicleContextMenuHandler, '__init__')
def ResearchVehicleContextMenuHandler___init__(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)
    self._AbstractContextMenuHandler__handlers.update(_CMAdditionalHandlers)
    return ret


@overrideMethod(ResearchVehicleContextMenuHandler, '_generateOptions')
def ResearchVehicleContextMenuHandler__generateOptions(base, self, *args, **kwargs):
    options = base(self, *args, **kwargs)
    generate_cm_instance_options(self, self.getVehInvID(), options)
    return options


define_cm_handler_methods(ResearchVehicleContextMenuHandler, _CMAdditionalHandlers)
LOADED = True

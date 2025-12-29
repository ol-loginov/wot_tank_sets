import logging
from .events import overrideMethod, overrideClassMethod
from gui.impl.gen.view_models.views.lobby.hangar.sub_views.vehicle_filter_model import VehicleFilterModel
from openwg_gameface import gf_mod_inject

log = logging.getLogger(__name__)


@overrideMethod(VehicleFilterModel, '__init__')
def VehicleFilterModel__init__(base, self, *args, **kwargs):
    log.info("TankCarouselFilterPopover___init__")
    ret = base(self, *args, **kwargs)

    gf_mod_inject(self, 'VehicleFilterModel',
                  styles=[],
                  modules=['coui://gui/gameface/mods/mod_editable_tank_sets/VehicleFilterAddon.js'])
    return ret


LOADED = True

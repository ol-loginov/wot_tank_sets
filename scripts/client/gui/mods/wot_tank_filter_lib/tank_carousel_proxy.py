import logging

from gui.Scaleform.daapi.view.lobby.hangar.carousels import TankCarousel
from .events import overrideMethod

log = logging.getLogger(__name__)


@overrideMethod(TankCarousel, 'updateVehicles')
def tank_carousel__update_vehicles(base, self, *args, **kwargs):
    return base(self, *args, **kwargs)


TANK_CAROUSEL_PROXY = True

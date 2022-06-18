import logging

from gui.Scaleform.daapi.view.lobby.hangar.carousels.basic.tank_carousel import TankCarousel
from .events import overrideMethod

log = logging.getLogger(__name__)


@overrideMethod(TankCarousel, 'updateVehicles')
def TankCarousel_updateVehicles(base, self, *args, **kwargs):
    return base(self, *args, **kwargs)


@overrideMethod(TankCarousel, '_getInitialFilterVO')
def TankCarousel__getInitialFilterVO(base, self, *args, **kwargs):
    return base(self, *args, **kwargs)


LOADED = True

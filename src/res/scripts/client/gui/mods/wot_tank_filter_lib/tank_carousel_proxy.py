from gui.Scaleform.daapi.view.lobby.hangar.carousels import TankCarousel
from .events import *

log = logging.getLogger(__name__)


def advise():
    log.info('override methods...')

    @overrideMethod(TankCarousel, 'updateVehicles')
    def tank_carousel__update_vehicles(base, self, *args, **kwargs):
        return base(self, *args, **kwargs)

    log.info('override methods complete')

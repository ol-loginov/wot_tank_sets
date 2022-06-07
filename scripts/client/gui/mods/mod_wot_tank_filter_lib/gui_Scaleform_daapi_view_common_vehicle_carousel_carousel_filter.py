import logging

from gui.Scaleform.daapi.view.common.vehicle_carousel.carousel_filter import CarouselFilter
from .events import overrideMethod

log = logging.getLogger(__name__)


@overrideMethod(CarouselFilter, 'load')
def carousel_filter__load(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)
    return ret


@overrideMethod(CarouselFilter, 'update')
def carousel_filter__update(base, self, *args, **kwargs):
    params = args[0]
    return base(self, *args, **kwargs)


LOADED = True

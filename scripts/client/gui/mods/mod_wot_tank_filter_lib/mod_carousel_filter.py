import logging

from gui.Scaleform.daapi.view.common.vehicle_carousel.carousel_filter import CarouselFilter
from .events import overrideMethod

log = logging.getLogger(__name__)


@overrideMethod(CarouselFilter, 'load')
def carousel_filter__load(base, self, *args, **kwargs):
    return base(self, *args, **kwargs)


CAROUSEL_FILTER_MODIFIED = True

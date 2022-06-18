import logging

# from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
# from account_helpers.AccountSettings import AccountSettings, DEFAULT_VALUES, KEY_FILTERS

from gui.Scaleform.daapi.view.common.vehicle_carousel.carousel_filter import CarouselFilter
from .events import overrideMethod

log = logging.getLogger(__name__)


@overrideMethod(CarouselFilter, 'load')
def carousel_filter__load(base, self, *args, **kwargs):
    # log.info("id(DEFAULT_VALUES[KEY_FILTERS])" + str(id(DEFAULT_VALUES[KEY_FILTERS])))
    return base(self, *args, **kwargs)


@overrideMethod(CarouselFilter, 'update')
def carousel_filter__update(base, self, *args, **kwargs):
    return base(self, *args, **kwargs)


LOADED = True

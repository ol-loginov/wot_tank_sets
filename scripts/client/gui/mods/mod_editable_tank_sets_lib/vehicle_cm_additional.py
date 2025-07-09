from logging import getLogger

from .settings import Settings as S
from .events import add_attr
from .l10n import l10n

log = getLogger(__name__)

_TankCarouselLast = None


class SUBMENU:
    MENU_ADD_TO_TC = 'add_to_user_tc'
    MENU_REMOVE_FROM_TC = 'remove_from_user_tc'

    ADD = 'addTankToTankCollection_'
    REMOVE = 'removeTankFromTankCollection_'
    REMOVE_FROM_ALL = 'removeTankFromTankCollections'

    @staticmethod
    def add(n): return SUBMENU.ADD + str(n)

    @staticmethod
    def remove(n): return SUBMENU.REMOVE + str(n)


def _addTank(self, n):
    S.add_tank_to_collection(n, self.getVehInvID())


def _removeTank(self, n):
    S.remove_tank_from_collection(n, self.getVehInvID())
    _refreshCarousel()


def _removeTankFromAll(self):
    S.remove_tank_from_all_collections(self.getVehInvID())
    _refreshCarousel()


def _refreshCarousel():
    try:
        if _TankCarouselLast is not None:
            current_setup = _TankCarouselLast.filter.getFilters()
            _TankCarouselLast.filter.update(current_setup, save=False)
            _TankCarouselLast.applyFilter()
    except:
        log.exception('cannot update carousel')


def setLastCarousel(carousel):
    global _TankCarouselLast
    _TankCarouselLast = carousel


# add menu commands
def define_cm_handler_methods(clazz, handlers):
    def add_menu_and_method(method_name, method_func):
        add_attr(clazz, method_name, method_func)
        handlers.update({method_name: method_name})

    for n in S.get_tc_numbers_all():
        add_menu_and_method(SUBMENU.add(n), lambda s, nn=n: _addTank(s, nn))
        add_menu_and_method(SUBMENU.remove(n), lambda s, nn=n: _removeTank(s, nn))
    add_menu_and_method(SUBMENU.REMOVE_FROM_ALL, lambda s: _removeTankFromAll(s))


def generate_cm_instance_options(instance, veh_inv_id, options):
    """
    :param SimpleVehicleCMHandler instance:
    :param veh_inv_id:
    :param options:
    :return:
    """
    if S.is_mod_enabled() and veh_inv_id is not None and veh_inv_id > 0:
        submenu_add = []
        submenu_remove = []
        for n, collection in S.get_enabled_collections():
            if veh_inv_id not in collection.tanks:
                submenu_add.append(instance._makeItem(SUBMENU.add(n), collection.title))
            if veh_inv_id in collection.tanks:
                submenu_remove.append(instance._makeItem(SUBMENU.remove(n), collection.title))

        if len(submenu_add) > 0:
            options.append(instance._makeItem(SUBMENU.MENU_ADD_TO_TC, l10n("menu.ADD_TO_TC"), optSubMenu=submenu_add))

        if len(submenu_remove) > 1:
            submenu_remove.insert(0, instance._makeItem(SUBMENU.REMOVE_FROM_ALL, l10n("menu.REMOVE_FROM_ALL")))
        if len(submenu_remove) > 0:
            item_label = l10n("menu.REMOVE_FROM_TC")
            item = instance._makeItem(SUBMENU.MENU_REMOVE_FROM_TC, item_label, optSubMenu=submenu_remove)
            options.append(item)

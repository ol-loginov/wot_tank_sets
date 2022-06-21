from gui.Scaleform.daapi.view.lobby.hangar.hangar_cm_handlers import VehicleContextMenuHandler
from .events import overrideMethod, add_attr
from .settings import Settings as S

MENU_ADD_TO_TC = 'add_to_user_tc'
MENU_REMOVE_FROM_TC = 'remove_from_user_tc'


class SUBMENU:
    ADD = 'addTankToTankCollection_'
    REMOVE = 'removeTankFromTankCollection_'
    REMOVE_FROM_ALL = 'removeTankFromTankCollections'

    @staticmethod
    def add(n): return SUBMENU.ADD + str(n)

    @staticmethod
    def remove(n): return SUBMENU.REMOVE + str(n)


VehicleContextMenuHandlerAdditionalFilters = {}


def _addTank(self, n):
    S.add_tank_to_collection(n, self.getVehInvID())


def _removeTank(self, n):
    S.remove_tank_from_collection(n, self.getVehInvID())


def _removeTankFromAll(self):
    S.remove_tank_from_all_collections(self.getVehInvID())


@overrideMethod(VehicleContextMenuHandler, '__init__')
def VehicleContextMenuHandler___init__(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)
    self._AbstractContextMenuHandler__handlers.update(VehicleContextMenuHandlerAdditionalFilters)
    return ret


@overrideMethod(VehicleContextMenuHandler, '_generateOptions')
def VehicleContextMenuHandler__generateOptions(base, self, *args, **kwargs):
    options = base(self, *args, **kwargs)

    veh_inv_id = self.getVehInvID()
    if veh_inv_id is not None:
        submenu_add = []
        submenu_remove = []
        for n, collection in S.get_enabled_collections():
            if veh_inv_id not in collection.tanks:
                submenu_add.append(self._makeItem(SUBMENU.add(n), collection.title))
            if veh_inv_id in collection.tanks:
                submenu_remove.append(self._makeItem(SUBMENU.remove(n), collection.title))

        if len(submenu_add) > 0:
            options.append(self._makeItem(MENU_ADD_TO_TC, MENU_ADD_TO_TC, optSubMenu=submenu_add))

        if len(submenu_remove) > 1:
            submenu_remove.insert(0, self._makeItem(SUBMENU.REMOVE_FROM_ALL, SUBMENU.REMOVE_FROM_ALL))
        if len(submenu_remove) > 0:
            options.append(self._makeItem(MENU_REMOVE_FROM_TC, MENU_REMOVE_FROM_TC, optSubMenu=submenu_remove))
    return options


# add menu commands
def add_context_menu_handler_methods():
    def add_menu_and_method(method_name, method_func):
        add_attr(VehicleContextMenuHandler, method_name, method_func)
        VehicleContextMenuHandlerAdditionalFilters.update({method_name: method_name})

    for n in S.get_tc_numbers_all():
        add_menu_and_method(SUBMENU.add(n), lambda s, n=n: _addTank(s, n))
        add_menu_and_method(SUBMENU.remove(n), lambda s, n=n: _removeTank(s, n))
    add_menu_and_method(SUBMENU.REMOVE_FROM_ALL, lambda s: _removeTankFromAll(s))


add_context_menu_handler_methods()
LOADED = True

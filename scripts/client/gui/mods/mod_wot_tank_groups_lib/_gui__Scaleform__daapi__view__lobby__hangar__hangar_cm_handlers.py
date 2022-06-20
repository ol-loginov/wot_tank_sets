from gui.Scaleform.daapi.view.lobby.hangar.hangar_cm_handlers import VehicleContextMenuHandler
from .events import overrideMethod
from .settings import Settings as S

MENU_ADD_TO_TC = 'add_to_user_tc'
MENU_REMOVE_FROM_TC = 'remove_from_user_tc'


@overrideMethod(VehicleContextMenuHandler, '_generateOptions')
def VehicleContextMenuHandler__generateOptions(base, self, *args, **kwargs):
    options = base(self, *args, **kwargs)

    veh_inv_id = self.getVehInvID()

    submenu_add = []
    submenu_remove = []
    for n, collection in S.get_enabled_collections():
        if veh_inv_id not in collection.tanks:
            submenu_add.append(self._makeItem(MENU_ADD_TO_TC, collection.title))
        if veh_inv_id in collection.tanks:
            submenu_remove.append(self._makeItem(MENU_REMOVE_FROM_TC, collection.title))

    if len(submenu_add) > 0:
        options.append(self._makeItem(MENU_ADD_TO_TC, MENU_ADD_TO_TC, optSubMenu=submenu_add))
    if len(submenu_remove) > 0:
        options.append(self._makeItem(MENU_REMOVE_FROM_TC, MENU_REMOVE_FROM_TC, optSubMenu=submenu_remove))

    return options


LOADED = True

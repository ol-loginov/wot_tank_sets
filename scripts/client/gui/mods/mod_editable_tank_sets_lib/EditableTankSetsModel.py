import json
import logging

from frameworks.wulf import ViewModel
from gui.impl.lobby.hangar.presenters.vehicle_filters_presenter import VehicleFiltersDataProvider
from openwg_gameface import gf_mod_inject
from .events import overrideMethod
from .l10n import l10n
from .settings import Settings as S

log = logging.getLogger(__name__)

VIEW_ID = 'EditableTankSets'


class EditableTankSetsModel(ViewModel):
    def __init__(self, properties=5, commands=1):
        self.checkpoint = 0
        super(EditableTankSetsModel, self).__init__(properties=properties, commands=commands)

    def getCollections(self):
        return self._getString(0)

    def setCollections(self, value):
        self._setString(0, value)

    def getModEnabled(self):
        return self._getBool(1)

    def setModEnabled(self, value):
        self._setBool(1, value)

    def setVisibleSet(self, value):
        self._setString(3, value)

    def setCheckpoint(self, value):
        self._setNumber(4, value)

    def _initialize(self):
        super(EditableTankSetsModel, self)._initialize()
        state = self.collect_state()
        log.info('load initial state: %s' % (json.dumps(state)))

        self._addStringProperty('collections', state['collections'])
        self._addBoolProperty('modEnabled', state['modEnabled'])
        self._addStringProperty('groupTitle', state['groupTitle'])
        self._addStringProperty('visibleSet', state['visibleSet'])
        self._addNumberProperty('checkpoint', self.checkpoint)
        self.onSave = self._addCommand('onSave')

    def on_save_callback(self, param):
        S.set_active_collections(json.loads(param.get('actives')))
        # self._itemsCache.onSyncCompleted(CACHE_SYNC_REASON.SHOP_RESYNC, {})

    def collect_state(self):
        collections = list()
        tanks = set()
        for n, collection in S.get_enabled_collections():
            collections.append({
                'n': n,
                'title': collection.title,
                # 'icon': collection.icon,
                'active': collection.active
            })
            if collection.active:
                tanks |= set(collection.tanks)

        return {
            'collections': json.dumps(collections),
            'modEnabled': S.is_mod_enabled(),
            'groupTitle': l10n("filterPopover.groupTitle"),
            'visibleSet': json.dumps(list(tanks) if S.has_active_collections() else None)
        }

    def load_state(self):
        self.checkpoint += 1
        state = self.collect_state()
        log.info('load new state: %s' % (json.dumps(state)))
        with self.transaction() as model:
            model.setCheckpoint(self.checkpoint)
            model.setCollections(state['collections'])
            model.setModEnabled(state['modEnabled'])
            # model.setVisibleSet(state['visibleSet'])
            # self._itemsCache.onSyncCompleted(CACHE_SYNC_REASON.SHOP_RESYNC, {})


# noinspection PyPep8Naming
@overrideMethod(VehicleFiltersDataProvider, '__init__')
def VehicleFiltersDataProvider___init__(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)
    if type(self) is not VehicleFiltersDataProvider:
        return ret

    log.info("add EditableTankSets viewModel into %s" % (type(self),))

    setattr(self, 'editableTankSetsModel', EditableTankSetsModel())
    self.viewModel._addViewModelProperty('EditableTankSets', self.editableTankSetsModel)
    gf_mod_inject(self.viewModel, 'VehicleFilterModel',
                  styles=['coui://gui/gameface/mods/mod_editable_tank_sets/EditableTankSets.css'],
                  modules=['coui://gui/gameface/mods/mod_editable_tank_sets/EditableTankSets.js'])

    return ret


@overrideMethod(VehicleFiltersDataProvider, '_getEvents')
def VehicleFiltersDataProvider_getEvents(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)
    if type(self) is not VehicleFiltersDataProvider:
        return ret

    log.info("subscribe EditableTankSets viewModel events")

    return ret + (
        (self.editableTankSetsModel.onSave, self.editableTankSetsModel.on_save_callback),
        (S.onChanged, self.editableTankSetsModel.load_state),
    )


LOADED = True
